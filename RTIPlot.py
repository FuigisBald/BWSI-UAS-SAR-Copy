import matplotlib.pyplot as plt
import numpy as np

#Speed of light 
c = 299,792,458

#Sample data from deepseek
ranges = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
amplitude = np.array([[10, 15, 20, 25, 30, 25, 20, 15, 10, 5],
            [12, 17, 22, 27, 32, 27, 22, 17, 12, 7],
            [8, 13, 18, 23, 28, 23, 18, 13, 8, 3],
            [15, 20, 25, 30, 35, 30, 25, 20, 15, 10],
            [5, 10, 15, 20, 25, 20, 15, 10, 5, 1],
            [20, 25, 30, 35, 40, 35, 30, 25, 20, 15],
            [7, 12, 17, 22, 27, 22, 17, 12, 7, 2],
            [18, 23, 28, 33, 38, 33, 28, 23, 18, 13],
            [3, 8, 13, 18, 23, 18, 13, 8, 3, -2],
            [25, 30, 35, 40, 45, 40, 35, 30, 25, 20]])

#Converts the amplitude array into decibels
db = 20 * np.log10(np.abs(amplitude))

#Converts the test data into a 3d Array
arr = []
for i in range(10):
    zist=[]
    for j in range(10):
        Z=db[i,j]
        zist.append(Z)
    arr.append(zist)    
arr = np.array(arr)

#Plots the data
plt.imshow(arr, aspect='equal')
plt.xticks(range(len(ranges)), ranges)
plt.yticks(range(10))
plt.colorbar()
plt.show()
