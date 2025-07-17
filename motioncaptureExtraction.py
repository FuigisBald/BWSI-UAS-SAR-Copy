import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import UnivariateSpline
import numpy as np
import csv
import pandas as pd

df = pd.read_csv('SARMotion.csv')

# Drop rows with any missing values
df_clean = df.dropna()

# If you want a NumPy array:
arr = df_clean.to_numpy()

#Pulls data from csv
t = arr[:, 0]
x = arr[:, 1]
y = arr[:, 3]
z = arr[:, 2]


#Manual offsets for back projection and RTI
tOffset = 0
xOffset = 0
yOffset = 0
zOffset = 0

t += tOffset
x += xOffset
y += yOffset
z += zOffset

#Function that creates a spline or LOBF for data.
def spline_regression(x, y, smoothing_factor=None):

    x = np.array(x)
    y = np.array(y)

    spline = UnivariateSpline(x, y, s=smoothing_factor)

    return spline

#Creates splines for x y and z variables
xSpline = spline_regression(t, x, 0.1)
ySpline = spline_regression(t, y, 0.1)
zSpline = spline_regression(t, z, 0.1)


# Makes 6000 estimates
tNew = np.linspace(min(t), max(t), 6000)

xNew = xSpline(tNew)
yNew = ySpline(tNew)
zNew = zSpline(tNew)

# # Create a new figure and add a 3D subplot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the 3D line
# ax.plot(x, y, z)
# ax.plot(xNew, yNew, zNew)

#Creates velocity splines using slope of the position splines
dxSpline = xSpline.derivative()
dySpline = ySpline.derivative()
dzSpline = zSpline.derivative()

dxNew = dxSpline(tNew)
dyNew = dySpline(tNew)
dzNew = dzSpline(tNew)


#Function that finds overallVelocity based on new time
def overallVelocity(timeNew):
    return np.sqrt(np.power(dxSpline(timeNew),2)+np.power(dySpline(timeNew),2)+np.power(dzSpline(timeNew),2))

# # Plots actual data
# plt.plot(t, x)
# plt.plot(t, y)
# plt.plot(t, z)

#Plots position splines
plt.plot(tNew, xNew, color = 'red')
plt.plot(tNew, yNew, color = 'blue')
plt.plot(tNew, zNew, color = 'green')

#Plots velocity splines 
plt.plot(tNew, dxNew, color = 'red')
plt.plot(tNew, dyNew, color = 'blue')
plt.plot(tNew, dzNew, color = 'green')
plt.plot(tNew, overallVelocity(tNew), color = 'black')

plt.show()
