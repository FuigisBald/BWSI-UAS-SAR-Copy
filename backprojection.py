import pickle
import matplotlib.pyplot as plt
import numpy as np

#Pulls data from file
with open('5_point_scatter.pkl', 'rb') as f:
    receivedData = pickle.load(f)

dataset = receivedData.get('scan_data')

print(dataset)

#plt.imshow(dataset, cmap = 'gray', aspect='auto', extent=(3, 50))

#plt.show()