import pickle
import matplotlib.pyplot as plt
import numpy as np 
import time
import os
from concurrent.futures import ProcessPoolExecutor
from matplotlib.widgets import Slider

def backprojection(pkl_path):
    """
    Generates a backprojection of the radar data for an offset    
    """
    
    # Pulls data from file
    with open(pkl_path, "rb") as f:
        receivedData = pickle.load(f)

    data_set = receivedData.get("scan_data")
    positions = receivedData.get("platform_pos")
    range_bins = receivedData.get("range_bins")
    scatters_pos = receivedData.get("scatters_pos")

    c_max_ranges = (scatters_pos[1][2]+0.2, scatters_pos[0][2]-0.4)  # x in meters, adjust as needed
    r_max_ranges = (scatters_pos[1][0]+0.2, scatters_pos[0][0]-0.2)
    grid_resolution = (500, 500)  # In pixels, adjust as needed
    # c_res = (c_max_range[1]-c_max_ranges[0]) / grid_resolution[1]  # Cross-range resolution
    # r_res = (r_max_ranges[1]-r_max_ranges[0]) / grid_resolution[0]  # Range resolution in meters

    # Create Cartesian coordinate grid w/ pixel values in meters
    x_coords = np.linspace(c_max_ranges[0], c_max_ranges[1], grid_resolution[1])
    y_coords = np.linspace(r_max_ranges[0], r_max_ranges[1], grid_resolution[0])
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    window = np.hanning(len(positions)) # Define Hanning window to correct haloing

    added_amplitudes = np.zeros(shape=(grid_resolution[0], grid_resolution[1]), dtype=complex)  # Base array for adding up intensities

    # Timer to track processing timex
    start_time = time.time()

    # Setting up multiprocessing
    num_processes = 12
    chunk_size = len(positions) // num_processes
    tasks = []

    print("Starting backprojection.")
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for p in range(num_processes):
           print(f"Spawned process {p+1}/{num_processes}")
           start = p * chunk_size # Split up frames across subprocesses
           end = len(positions) if p == num_processes - 1 else (p + 1) * chunk_size
           tasks.append(executor.submit(process_frames_chunk, start, end, grid_resolution, positions, data_set, range_bins, x_grid, y_grid, window)) # Submit tasks to executor

        partial_frames = [t.result() for t in tasks] # Get back summed frames from each subprocess

    final_frames = np.sum(partial_frames, axis=0)
    avg_final_frames = final_frames/len(positions) # Average out amplitudes based on number of frames
    
    back_projection_intensities = 20 * np.log10(np.abs(avg_final_frames)) # Convert to dB scale

    print(f"Finished processing in {time.time() - start_time:.2f}s.")

    return back_projection_intensities, c_max_ranges, r_max_ranges

def process_frames_chunk(start, end, grid_resolution, positions, data_set, range_bins, x_grid, y_grid, window):
    """
    Process a chunk of frames in parallel, and add up amplitudes of each frame in chunk.

    :param start: Index of the first frame in the chunk.
    :param end: Index of the last frame in the chunk.
    :return: Summed up amplitudes of the frames in the chunk.
    :rtype: numpy.ndarray
    """
    partial_frames = np.zeros(shape=(grid_resolution[0], grid_resolution[1]), dtype=complex)

    for i in range(start, end):
        partial_frames += process_frame(i, positions, data_set, range_bins, x_grid, y_grid, window) # Sum up chunk of frames in subprocess

    return partial_frames

def process_frame(frame_index, positions, data_set, range_bins, x_grid, y_grid, window):
    """Generate a single backprojection frame for a given frame index
    
    :param frame_index: Index of the frame to process.
    :return: Amplitudes of the frame.
    :rtype: numpy.ndarray
    """
    distances = np.sqrt(
        (positions[frame_index][2] - x_grid) ** 2 + # X Axis
        (positions[frame_index][0] - y_grid) ** 2 + # Y Axis
        positions[frame_index][1] ** 2 # Z Axis
    )
    local_amplitudes = np.interp(distances, range_bins, data_set[frame_index]) # Linear interpolation

    # Re-shift hilbert data
    local_amplitudes *= np.exp(4j * np.pi * distances * 4.3e9/299792458)
    weighted_amplitudes = local_amplitudes * window[frame_index] # Window amplitudes with Hanning window
    return weighted_amplitudes

def update(val):
    cutoff = slider.val
    for im, img in images:
        img_cut = np.clip(img, cutoff, img.max())
        im.set_data(img_cut)
        im.set_clim(cutoff, img.max())
    figure.canvas.draw_idle()

if __name__ == "__main__":
    figure, axis = plt.subplots(4,4)
    plt.subplots_adjust(bottom=0.2)  # Make space for slider

    images = []
    colorbars = []


    dir_path = "pickleoutputs/thur afternoon 6"
    pkl_paths = os.listdir(dir_path)
    for idx, path in enumerate(pkl_paths):
        y = idx // 4
        x = idx % 4
        img, c_max_ranges, r_max_ranges = backprojection(f"{dir_path}/{path}")
        im = axis[x, y].imshow(img, aspect='auto', extent=(c_max_ranges[0], c_max_ranges[1], r_max_ranges[0], r_max_ranges[1]), origin="lower")
        cb = figure.colorbar(im, ax=axis[x, y])
        axis[x, y].set_title(path)
        images.append((im, img))
        colorbars.append(cb)
    ax_slider = plt.axes([0.2, 0.08, 0.6, 0.03])
    min_intensity = min(img.min() for _, img in images)
    max_intensity = max(img.max() for _, img in images)
    slider = Slider(ax_slider, 'Min Intensity', 40, 60, valinit=40)


    slider.on_changed(update)
    plt.show()