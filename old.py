import pickle
import matplotlib.pyplot as plt
import numpy as np

#Pulls data from file
with open('5_point_scatter.pkl', 'rb') as f:
    receivedData = pickle.load(f)

data_set = receivedData.get('scan_data')
positions = receivedData.get('platform_pos')
range_bins = receivedData.get('range_bins')



#Single backprojection for first frame
drone_pos = (positions[0][0], positions[0][1], positions[0][2]) # Drone position for first frame
grid_resolution = (100, 100) # In pixels, adjust as needed
c_ranges = (-10, 10) # In meters, adjust as needed
r_ranges = (-10, 10)
r_res = (r_ranges[1]-r_ranges[0]) / grid_resolution[0] # Range resolution in meters
c_res = (c_ranges[1]-c_ranges[0]) / grid_resolution[1] # Cross-range resolution

# Getting the range bin index for each pixel in the backprojected image
# for cross_range in range(grid_resolution[0]):
#     for range_val in range(grid_resolution[1]):
#         pixel_coords = (cross_range, range_val)
#         pixel_coords_meters = (pixel_coords[0] * c_res, pixel_coords[1] * r_res)
#         distance = np.sqrt(
#             (pixel_coords_meters[0] - drone_pos[0]) ** 2 + # X Axis
#             (pixel_coords_meters[1] - drone_pos[1]) ** 2 + # Y Axis
#             (0 - drone_pos[2]) ** 2 # Z Axis (assuming ground level is 0)
#         )
    
#     distance_index = np.argmin(np.abs(range_bins - distance))
#     intensity = db_set[0][distance_index]
#     backprojected_intensities[cross_range][range_val] = intensity

# plt.imshow(
#     backprojected_intensities, extent=[0, max_ranges[0], 0, max_ranges[0]], cmap="inferno"
# )
# plt.colorbar(label='Amplitude (dB)')
# plt.show()
added_amplitudes =  np.zeros(shape=(grid_resolution[0], grid_resolution[1]))
for z in range(len(positions)):
    for j in range(grid_resolution[0]):
        for k in range(grid_resolution[1]):
            pixel_coords_meters = (j * c_res + c_ranges[0], k * r_res+ r_ranges[0])
            distance = np.sqrt((positions[z][0]-pixel_coords_meters[0])**2 + (positions[z][1]-pixel_coords_meters[1])**2 + positions[z][2]**2)
            index = np.argmin(np.abs(range_bins - distance))
            added_amplitudes[k][j] += data_set[z][index]
avg_amps = added_amplitudes/len(positions)
db_amps = 20 * np.log10(np.abs(avg_amps))

plt.imshow(avg_amps)
plt.show()


