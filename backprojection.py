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
