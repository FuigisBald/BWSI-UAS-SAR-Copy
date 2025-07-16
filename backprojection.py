import pickle
import matplotlib.pyplot as plt
import numpy as np 
import time
from concurrent.futures import ProcessPoolExecutor

# Pulls data from file
with open("C:/Users/thema/Downloads/marathon_18.pkl", "rb") as f:
    receivedData = pickle.load(f)

data_set = receivedData.get("scan_data")
positions = receivedData.get("platform_pos")
range_bins = receivedData.get("range_bins")

grid_resolution = (300, 300)  # In pixels, adjust as needed
c_max_ranges = (-73, -79)  # x in meters, adjust as needed
r_max_ranges = (-117, -112)  # y in meters, adjust as needed
c_res = (c_max_ranges[1]-c_max_ranges[0]) / grid_resolution[1]  # Cross-range resolution
r_res = (r_max_ranges[1]-r_max_ranges[0]) / grid_resolution[0]  # Range resolution in meters

x_coords = np.linspace(c_max_ranges[0], c_max_ranges[1], grid_resolution[1])
y_coords = np.linspace(r_max_ranges[0], r_max_ranges[1], grid_resolution[0])
x_grid, y_grid = np.meshgrid(x_coords, y_coords)

added_amplitudes = np.zeros(shape=(grid_resolution[0], grid_resolution[1]), dtype=complex)  # Base array for adding up intensities

def process_frames_chunk(start, end):
    partial_frames = np.zeros(shape=(grid_resolution[0], grid_resolution[1]), dtype=complex)

    for i in range(start, end):
        partial_frames += process_frame(i)

    return partial_frames

def process_frame(frame_index):
    """Compute amplitude image for one frame index z."""
    local_amplitudes = np.zeros((grid_resolution[0], grid_resolution[1]), dtype=complex)
    distances = np.sqrt(
        (positions[frame_index][0] - x_grid) ** 2 + # X Axis
        (positions[frame_index][1] - y_grid) ** 2 + # Y Axis
        positions[frame_index][2] ** 2 # Z Axis
    )

    local_amplitudes = np.interp(distances, range_bins, data_set[frame_index])
    return local_amplitudes

if __name__ == "__main__":
    # Timer to track processing time
    start_time = time.time()

    # Setting up multiprocessing

    num_processes = 12
    chunk_size = len(positions) // num_processes
    tasks = []

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for p in range(num_processes):
           start = p * chunk_size
           end = len(positions) if p == num_processes - 1 else (p + 1) * chunk_size
           tasks.append(executor.submit(process_frames_chunk, start, end))

        partial_frames = [t.result() for t in tasks]

    final_frames = np.sum(partial_frames, axis=0)
    
    back_projection_intensities = 20 * np.log10(np.abs(final_frames))  # Convert to dB scale
    print(f"Processing time: {time.time() - start_time:.2f} seconds")

    #back_projection_intensities /= 200 # Normalize 
    plt.imshow(
        back_projection_intensities,
        aspect = 'auto',
        extent=(c_max_ranges[0], c_max_ranges[1], r_max_ranges[0], r_max_ranges[1]),
        origin="lower",
    )
    plt.colorbar(label="Intensity (dB)")
    plt.title("Backprojection of Radar Data")
    plt.xlabel("Cross-range (m)")
    plt.ylabel("Range (m)")
    plt.show()