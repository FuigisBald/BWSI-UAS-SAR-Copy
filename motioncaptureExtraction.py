import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import UnivariateSpline
import numpy as np
import csv

# Example: skip the header row
arr = np.genfromtxt('SARMotion.csv', delimiter=',', skip_header=1)

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
    """
    Fits a spline regression to the given x and y data.

    Parameters:
        x (list or array): list of x-values
        y (list or array): list of y-values
        smoothing_factor (float, optional): smoothing factor s.
            If None, it will be estimated automatically.

    Returns:
        spline_func (function): a function that takes new x-values and returns the spline-predicted y-values.
    """
    # Convert to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Fit spline
    spline = UnivariateSpline(x, y, s=smoothing_factor)

    return spline

xSpline = spline_regression(t, x)
ySpline = spline_regression(t, y)
zSpline = spline_regression(t, z)

# Make predictions
xNew = xSpline(t)
yNew = ySpline(t)
zNew = zSpline(t)

print(xNew)
print(yNew)
print(zNew)

# Create a new figure and add a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D line
ax.plot(x, y, z)
ax.plot(xNew, yNew, zNew)

plt.show()