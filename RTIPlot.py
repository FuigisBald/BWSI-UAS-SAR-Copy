import matplotlib.pyplot as plt
import numpy as np

#Speed of light 
c = 299,792,458

#Sample data from deepseek

 
ranges = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

intensity = np.array([[10, 15, 20, 25, 30, 25, 20, 15, 10, 5],
            [12, 17, 22, 27, 32, 27, 22, 17, 12, 7],
            [8, 13, 18, 23, 28, 23, 18, 13, 8, 3],
            [15, 20, 25, 30, 35, 30, 25, 20, 15, 10],
            [5, 10, 15, 20, 25, 20, 15, 10, 5, 0],
            [20, 25, 30, 35, 40, 35, 30, 25, 20, 15],
            [7, 12, 17, 22, 27, 22, 17, 12, 7, 2],
            [18, 23, 28, 33, 38, 33, 28, 23, 18, 13],
            [3, 8, 13, 18, 23, 18, 13, 8, 3, -2],
            [25, 30, 35, 40, 45, 40, 35, 30, 25, 20]])
arr = []
#Prints all elements of 3D
for i in range(10):
    zist=[]
    for j in range(10):
        Z=intensity[i,j]
        zist.append(Z)
    arr.append(zist)    

arr = np.array(arr)
print(arr)

plt.imshow(arr, aspect='equal')
plt.xticks(range(len(ranges)), ranges)
plt.yticks(range(10))
plt.colorbar()
plt.show()

"""
def convertToDecibles():

def findIntensity():
    point = intensity[0, 0]
    print(point)
"""