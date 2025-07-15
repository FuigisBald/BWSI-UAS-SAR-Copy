import pickle
import matplotlib.pyplot as plt
import numpy as np

#Pulls data from file
with open('5_point_scatter.pkl', 'rb') as f:
    receivedData = pickle.load(f)

data_set = receivedData.get('scan_data')
positions = receivedData.get('platform_pos')
range_bins = receivedData.get('range_bins')

db_set = 20 * np.log10(np.abs(data_set))

#Single backprojection for first frame
drone_pos = (positions[0][0], positions[0][1], positions[0][2]) # Drone position for first frame
grid_resolution = (100, 100) # In pixels, adjust as needed
max_ranges = (10, 10) # In meters, adjust as needed
backprojected_intensities = np.empty(grid_resolution)
r_res = max_ranges[0] / grid_resolution[0] # Range resolution in meters
c_res = max_ranges[1] / grid_resolution[1] # Cross-range resolution

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
            distance = np.sqrt((positions[z][0]-j)**2 + (positions[z][1]-k)**2 + positions[z][2]**2)
            for i in range (len(range_bins)):
                if(range_bins[i] > distance):
                    if(np.abs(range_bins[i-1] - distance) > np.abs(range_bins[i] - distance)):
                        index = i-1
                    else:
                        index = i
                    break
            added_amplitudes[j][k] += data_set[z][index]

plt.imshow(added_amplitudes)
plt.show()

# # RPI Plot
# plt.imshow(db_set, aspect='auto', extent=[range_bins[0], range_bins[-1], positions[0][0], positions[-1][0]], cmap="inferno")
# plt.colorbar(label='Amplitude (dB)')
# plt.xlabel('Range (m)')
# plt.ylabel('Position (m)')
# plt.title('RPI')
# plt.show()

# Scatter plot of the first frame
# plt.scatter(range_bins, data_set[1], s=1)
# plt.show() #multiple db_set[0] values for every range_bins value

# This code is for adding up amplitudes. Probably won't need it and just delete it but im keeping it here just in case

# backprojected_intensities = db_set[0]
# for j in range (len(db_set)-1):
#     for i in range (len(db_set[0])):
#         backprojected_intensities[i] += db_set[j+1][i]

# print(backprojected_intensities)

# plt.scatter(backprojected_intensities, range_bins, color='red', label="Data Points") 
# plt.show()
# """