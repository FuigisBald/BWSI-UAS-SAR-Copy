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

t = arr[:, 0]
x = arr[:, 1]
y = arr[:, 3]
z = arr[:, 2]

tOffset = 0
xOffset = 0
yOffset = 0
zOffset = 0

t += tOffset
x += xOffset
y += yOffset
z += zOffset

def spline_regression(x, y, smoothing_factor=None):

    x = np.array(x)
    y = np.array(y)

    spline = UnivariateSpline(x, y, s=smoothing_factor)

    return spline

xSpline = spline_regression(t, x, 0.1)
ySpline = spline_regression(t, y, 0.1)
zSpline = spline_regression(t, z, 0.1)

# # Make predictions
tNew = np.linspace(min(t), max(t), 10000)

xNew = xSpline(tNew)
yNew = ySpline(tNew)
zNew = zSpline(tNew)

# # Create a new figure and add a 3D subplot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the 3D line
# ax.plot(x, y, z)
# ax.plot(xNew, yNew, zNew)

plt.plot(t, x)
plt.plot(t, y)
plt.plot(t, z)

plt.plot(tNew, xNew)
plt.plot(tNew, yNew)
plt.plot(tNew, zNew)

plt.show()