import pickle
import matplotlib.pyplot as plt
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor

# Pulls data from file
with open("5_point_scatter.pkl", "rb") as f:
    receivedData = pickle.load(f)

data_set = receivedData.get("scan_data")
positions = receivedData.get("platform_pos")
range_bins = receivedData.get("range_bins")

grid_resolution = (100, 100)  # In pixels, adjust as needed
c_max_ranges = (-25, 25)  # x in meters, adjust as needed
r_max_ranges = (-25, 25)  # y in meters, adjust as needed
c_res = (c_max_ranges[1]-c_max_ranges[0]) / grid_resolution[1]  # Cross-range resolution
r_res = (r_max_ranges[1]-r_max_ranges[0]) / grid_resolution[0]  # Range resolution in meters

x_coords = np.linspace(c_max_ranges[0], c_max_ranges[1], grid_resolution[1])
y_coords = np.linspace(r_max_ranges[0], r_max_ranges[1], grid_resolution[0])
x_grid, y_grid = np.meshgrid(x_coords, y_coords)

added_amplitudes = np.zeros(shape=(grid_resolution[0], grid_resolution[1]), dtype=complex)  # Base array for adding up intensities

def process_frame(frame_index):
    """Compute amplitude image for one frame index z."""
    local_amplitudes = np.zeros((grid_resolution[0], grid_resolution[1]), dtype=complex)
    print(f"Processing frame {frame_index + 1}/{len(positions)}")
    distances = np.sqrt(
        (positions[frame_index][0] - x_grid) ** 2 + # X Axis
        (positions[frame_index][1] - y_grid) ** 2 + # Y Axis
        positions[frame_index][2] ** 2 # Z Axis
    )
    bin_indices = np.argmin(np.abs(range_bins - distances[:, :, np.newaxis]), axis=-1)  # Find index of the closest range bin
    local_amplitudes = data_set[frame_index][bin_indices]
    return local_amplitudes

if __name__ == "__main__":
    # Timer to track processing time
    start_time = time.time()

    with ProcessPoolExecutor() as executor:
       results = list(executor.map(process_frame, range(len(positions))))

    added_amplitudes = np.sum(results)
    
    back_projection_intensities = 20 * np.log10(np.abs(added_amplitudes))  # Convert to dB scale
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