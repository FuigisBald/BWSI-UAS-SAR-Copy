import pickle
import matplotlib.pyplot as plt
import numpy as np

#Pulls data from file
with open('5_point_scatter.pkl', 'rb') as f:
    receivedData = pickle.load(f)
print(receivedData)
data_set = receivedData.get('scan_data')
positions = receivedData.get('platform_pos')
range_bins = receivedData.get('range_bins')

db_set = 20 * np.log10(np.abs(data_set))

#Single backprojection for first frame
drone_pos = (positions[0][0], positions[0][1], positions[0][2]) # Drone position for first frame
grid_resolution = (100, 100) # In pixels, adjust as needed
max_ranges = (-50, 50) # In meters, adjust as needed
backprojected_intensities = np.empty(grid_resolution)
r_res = max_ranges[0] / grid_resolution[0] # Range resolution in meters
c_res = max_ranges[1] / grid_resolution[1] # Cross-range resolution

added_amplitudes =  np.zeros(shape=(grid_resolution[0], grid_resolution[1]))
for z in range(len(positions)):
    for j in range(grid_resolution[0]):
        for k in range(grid_resolution[1]):
            pixel_coords_meters = ((j* c_res-25)/1.5, (k * r_res+25)/1.5) #the second one changes x and the first changes y
            distance = np.sqrt((positions[z][0]-pixel_coords_meters[0])**2 + (positions[z][1]-pixel_coords_meters[1])**2 + positions[z][2]**2)
            index = np.argmin(np.abs(range_bins - distance))
            added_amplitudes[j][k] += db_set[z][index]

avg_amps = added_amplitudes/len(positions)
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