import matplotlib.pyplot as plt
import numpy as np

#Speed of light 
c = 299,792,458*10^-12

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

#Sample data from deepseek transformed into how we will actually be receiving the data
receivedAmplitude = np.array([[0.1, [10, 15, 20, 25, 30, 25, 20, 15, 10, 5]], [0.2,[12, 17, 22, 27, 32, 27, 22, 17, 12, 7]], [0.3,[8, 13, 18, 23, 28, 23, 18, 13, 8, 3]],
[0.4,[15, 20, 25, 30, 35, 30, 25, 20, 15, 10]], [0.5, [5, 10, 15, 20, 25, 20, 15, 10, 5, 1]],
[0.6,[20, 25, 30, 35, 40, 35, 30, 25, 20, 15]], [0.7,[7, 12, 17, 22, 27, 22, 17, 12, 7, 2]], [0.8,[18, 23, 28, 33, 38, 33, 28, 23, 18, 13]], [0.9,[25, 30, 35, 40, 45, 40, 35, 30, 25, 20]]])

#Converts the amplitude array into decibels
db = 20 * np.log10(np.abs(amplitude))

#Converts the test data into a 3d Array -> we don't need this yet. Could be useful for when we get the data and try to convert into what we have above

arr = []
for i in range(len(amplitude)):
    zist=[]
    for j in range(len(amplitude[0])):
        Z=db[j,i]
        zist.append(Z)
    arr.append(zist)    
arr = np.array(arr)
print (arr)


#Plots the data
plt.imshow(arr, aspect='equal')
plt.xticks(range(len(ranges)), ranges)
plt.yticks(range(10))
plt.colorbar()
plt.savefig("FirstRTIPlot.png")
plt.show()

