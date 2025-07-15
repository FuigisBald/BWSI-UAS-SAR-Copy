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

# Single backprojection for first frame
drone_pos = (positions[0][0], positions[0][1], positions[0][2]) # Drone position for first frame
grid_resolution = (250, 250) # In pixels, adjust as needed
ranges = ((-100, 100), (-100, 100)) # In meters, adjust as needed
r_res = ranges[0][1] / grid_resolution[0] # Range resolution in meters
c_res = ranges[1][1] / grid_resolution[1] # Cross-range resolution
backprojected_intensities = np.empty(grid_resolution)

# Getting the range bin index for each pixel in the backprojected image
for cross_range in range(grid_resolution[0]):
    for range_val in range(grid_resolution[1]):
        pixel_coords = (cross_range, range_val)
        pixel_coords_meters = (pixel_coords[0] * r_res + drone_pos[0]*3, pixel_coords[1] * c_res + drone_pos[1]*1.5 + ranges[0][0]/2)

        distance = np.sqrt(
            (pixel_coords_meters[0] - drone_pos[0]) ** 2 + # X Axis
            (pixel_coords_meters[1] - drone_pos[1]) ** 2 + # Y Axis
            (0 - drone_pos[2]) ** 2 # Z Axis (assuming ground level is 0)
        )
    
        distance_index = np.argmin(np.abs(range_bins - distance))
        intensity = db_set[0][distance_index]

        backprojected_intensities[range_val][cross_range] = intensity

plt.imshow(
    backprojected_intensities, extent=[ranges[0][0], ranges[0][1], ranges[1][0], ranges[0][1]], cmap="inferno"
)
plt.colorbar(label='Amplitude (dB)')
plt.scatter(
    [drone_pos[0]], [drone_pos[1]], color='blue', label='Drone Position'    
)
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