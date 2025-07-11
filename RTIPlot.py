import matplotlib.pyplot as plt
import numpy as np
import json

#Pulls data from json file
with open('scans-2024-06-26_23-07-29.json', 'r') as f:
    receivedData = json.load(f)

#Sample data from deepseek transformed into how we will actually be receiving the data
receivedAmplitude = []
longTime = []
for i in range (len(receivedData)):
    receivedAmplitude.append(receivedData[i][1])
    longTime.append(receivedData[i][0])

#If we set range scale, we avoid a massive 3d array with a lot of repeating data points.
#We can still get the same RTI graph by just setting the scale seperately
rangeScale = ((len(receivedData[0][1])*61+300)*299792458*(10e-13))/2

#Converts the amplitude array into decibels
db = 20 * np.log10(np.abs(receivedAmplitude))

#Plots the data
plt.imshow(db, aspect='auto', extent=(0, rangeScale, receivedData[0][0], (receivedData[-1][0])))
plt.colorbar()
plt.show()