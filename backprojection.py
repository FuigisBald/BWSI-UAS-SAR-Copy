import pickle
import matplotlib.pyplot as plt
import numpy as np

#Pulls data from file
with open('5_point_scatter.pkl', 'rb') as f:
    receivedData = pickle.load(f)

amplitudes = receivedData.get('scan_data') #200 lists of 2551 amplitudes
rangebins = receivedData.get('range_bins') #2551 range bins
location = receivedData.get('platform_pos') #200 locations

#Converts the amplitude array into decibels
db = 20 * np.log10(np.abs(amplitudes))

circent = (-20,-15) #hardcoded location of drone
colormap = plt.colormaps['viridis']
#max = 90
#min = -30 this is around what I found for the first frame, could be changed or shifted etc
fig, ax = plt.subplots()

for i in range(len(rangebins)):
    amp = db[0][i] #hardcoded 0 for the first frame, change for integration
    circ = plt.Circle(circent,rangebins[i],fill=False,color=colormap((amp+30)/(120))) #fix hardcoded min and max
    ax.add_patch(circ)

ax.set_xlim(-50, 50) #find a more reasonable plot size
ax.set_ylim(-50, 50)
ax.set_aspect('equal')
#plt.colorbar()
plt.show()

""""
could keep or delete, I just didn't want to delete it while merging...
data_set = receivedData.get('scan_data')
position = receivedData.get('platform_pos')
range_bins = receivedData.get('range_bins')
print(len(range_bins)) #prints 2551
db_set= 20 * np.log10(np.abs(data_set))
print(len(data_set[1])) #prints 2551
print(data_set[1])
print("data_set shape:", np.array(data_set).shape)  
print("range_bins shape:", np.array(range_bins).shape)
plt.scatter(range_bins, data_set[1], s=1)
plt.show() #multiple db_set[0] values for every range_bins value
"""
""""
This earlier gave a very clear graph but not sure if relavent to what we gotta do. im just commenting it out for now

plt.imshow(db_set, aspect='auto', extent=[#xstart ystart, range_bins[0], range_bins[-1]])
plt.show()
"""

"""

This code is for adding up amplitudes. Probably won't need it and just delete it but im keeping it here just in case

backprojected_amplitudes = db_set[0]
for j in range (len(db_set)-1):
    for i in range (len(db_set[0])):
        backprojected_amplitudes[i] += db_set[j+1][i]

print(backprojected_amplitudes)

plt.scatter(backprojected_amplitudes, range_bins, color='red', label="Data Points") 
plt.show()
"""
