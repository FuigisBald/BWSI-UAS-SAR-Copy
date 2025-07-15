import pickle
import matplotlib.pyplot as plt
import numpy as np
import time

# Timer to track processing time
start_time = time.time()

# Pulls data from file
with open("5_point_scatter.pkl", "rb") as f:
    receivedData = pickle.load(f)

data_set = receivedData.get("scan_data").real
positions = receivedData.get("platform_pos")
range_bins = receivedData.get("range_bins")

# Single backprojection for first frame
drone_pos = (
    positions[0][0],
    positions[0][1],
    positions[0][2],
)  # Drone position for first frame
grid_resolution = (100, 100)  # In pixels, adjust as needed
max_ranges = (-50, 50)  # In meters, adjust as needed
r_res = max_ranges[0] / grid_resolution[0]  # Range resolution in meters
c_res = max_ranges[1] / grid_resolution[1]  # Cross-range resolution

added_amplitudes = np.zeros(
    shape=(grid_resolution[0], grid_resolution[1])
)  # Base array for adding up intensities
for z in range(len(positions)):
    print(f"Processing frame {z + 1}/{len(positions)}")
    for j in range(grid_resolution[0]):
        for k in range(grid_resolution[1]):
            pixel_coords_meters = (
                j * c_res + (max_ranges[0] / 2),
                k * r_res + (max_ranges[1] / 2),
            )  # Converts pixel coordinates to meters
            # Calculate the distance from the drone to the pixel coordinates
            distance = np.sqrt(
                (positions[z][0] - pixel_coords_meters[0]) ** 2 + # X Axis
                (positions[z][1] - pixel_coords_meters[1]) ** 2 + # Y Axis
                positions[z][2] ** 2 # Z Axis
            )
            index = np.argmin(
                np.abs(range_bins - distance)
            )  # Find index of the closest range bin
            added_amplitudes[k][j] += data_set[z][index]  # Adds the amplitude at the pixel coordinates for each frame

back_projection_intensities = 20 * np.log10(np.abs(added_amplitudes))  # Convert to dB scale

#back_projection_intensities /= 200 # Normalize 
plt.imshow(
    back_projection_intensities,
    extent=(max_ranges[0] / 2, max_ranges[1] / 2, max_ranges[0] / 2, max_ranges[1] / 2),
    cmap="plasma",
    origin="lower",
)
plt.colorbar(label="Intensity (dB)")
plt.title("Backprojection of Radar Data")
plt.xlabel("Cross-range (m)")
plt.ylabel("Range (m)")
plt.show()