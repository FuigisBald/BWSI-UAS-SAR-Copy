import numpy as np
from scipy.interpolate import UnivariateSpline
import pandas as pd


# Need this function because adding functions diminishes the scope of key variables
def getSpline(csv):
    df = pd.read_csv(csv, skiprows = 6, usecols=[1, 20, 21, 22])

    # Drop rows with any missing values
    df_clean = df.dropna()

    # If you want a NumPy array:
    arr = df_clean.to_numpy()

    #Pulls data from csv
    t = arr[:, 0]
    x = arr[:, 1]
    y = arr[:, 2]
    z = arr[:, 3]

    #Manual offsets for back projection and RTI
    tOffset = 0
    xOffset = 0
    yOffset = 0
    zOffset = 0

    t += tOffset
    x += xOffset
    y += yOffset
    z += zOffset

    #Creates splines for x y and z variables

    xSpline = spline_regression(t, x, 0.1)
    ySpline = spline_regression(t, y, 0.1)
    zSpline = spline_regression(t, z, 0.1)
    return xSpline, ySpline, zSpline

#Function that creates a spline or LOBF for data.
def spline_regression(x, y, smoothing_factor=None):
    """
    Creates a spline or LOBF for data.
    :param x: x values
    :param y: y values
    :param smoothing_factor: smoothing factor
    :return: spline or LOBF
    """

    x = np.array(x)
    y = np.array(y)

    spline = UnivariateSpline(x, y, s=smoothing_factor)

    return spline


def distancesFromScatters(csv, scatterersPos):
    df = pd.read_csv(csv, skiprows = 6, usecols=[1, 20, 21, 22])

    # Drop rows with any missing values
    df_clean = df.dropna()

    # If you want a NumPy array:
    arr = df_clean.to_numpy()

    #Pulls data from csv
    t = arr[:, 0]
    x = arr[:, 1]
    y = arr[:, 2]
    z = arr[:, 3]

    #Creates splines for x y and z variables

    xSpline = spline_regression(t, x, 0.1)
    ySpline = spline_regression(t, y, 0.1)
    zSpline = spline_regression(t, z, 0.1)
    
    numEstimates = 6000

    # Makes 6000 estimates
    tNew = np.linspace(min(t), max(t), numEstimates)

    # xNew = xSpline(tNew)
    # yNew = ySpline(tNew)
    # zNew = zSpline(tNew)
    # # Create a new figure and add a 3D subplot
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D line
    # ax.plot(x, y, z)
    # ax.plot(xNew, yNew, zNew)

    toReturn = []
    for i in range(len(scatterersPos)):
        toAdd = []
        for j in range(numEstimates):
            toAdd.append(np.sqrt(np.power(xSpline(j/numEstimates*t[-1])-scatterersPos[i][0], 2) + 
                                 np.power(ySpline(j/numEstimates*t[-1])-scatterersPos[i][1], 2) + 
                                 np.power(zSpline(j/numEstimates*t[-1])-scatterersPos[i][2], 2)))
        toReturn.append(toAdd)
        toAdd = []

    return toReturn, tNew

def intepolate_positions(slow_times, mocap_path, offset):
    df = pd.read_csv(mocap_path, skiprows = 6, usecols=[1, 20, 21, 22])

    # Drop rows with any missing values
    df_clean = df.dropna()

    # If you want a NumPy array:
    arr = df_clean.to_numpy()

    #Pulls data from csv
    mocap_t = arr[:, 0]
    mocap_x = arr[:, 1]
    mocap_y = arr[:, 2]
    mocap_z = arr[:, 3]

    #Python returns the index of splines as arrays of no length but also have a float in it. It's weird but can be
    #fixed by simply typecasting
    interp_x = np.interp(slow_times, mocap_t+offset, mocap_x)
    interp_y = np.interp(slow_times, mocap_t+offset, mocap_y)
    interp_z = np.interp(slow_times, mocap_t+offset, mocap_z)
    return np.array([interp_x, interp_y, interp_z]).T

# True position from scatterer


# def distanceFromSingleScatter(timeNew, index):
#     return np.sqrt(np.power(xSpline(timeNew)-scatterersPos[index][0], 2) + np.power(ySpline(timeNew)-scatterersPos[index][1], 2) + np.power(zSpline(timeNew)-scatterersPos[index][2], 2))


# def distanceFromAllScatters(timeNew):
#     distances = []
#     for i in range (len(scatterersPos)):
#         distances.append(distanceFromSingleScatter(timeNew, i))
#     return distances

# def plotDistanceFromAllScatters(timeNew):
#     for i in range (len(distanceFromAllScatters(timeNew))):
#         plt.plot(distanceFromSingleScatter(timeNew, i), tNew, label = "Distance From Scatterer")



# # Create a new figure and add a 3D subplot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the 3D line
# ax.plot(x, y, z)
# ax.plot(xNew, yNew, zNew)

#Creates velocity splines using slope of the position splines
# dxSpline = xSpline.derivative()
# dySpline = ySpline.derivative()
# dzSpline = zSpline.derivative()

# dxNew = dxSpline(tNew)
# dyNew = dySpline(tNew)
# dzNew = dzSpline(tNew)


# #Function that finds overallVelocity based on new time
# def overallVelocity(timeNew):
#     return np.sqrt(np.power(dxSpline(timeNew),2)+np.power(dySpline(timeNew),2)+np.power(dzSpline(timeNew),2))

# Plots actual data
# plt.plot(t, x)
# plt.plot(t, y)
# plt.plot(t, z)

# plt.plot(tNew, xNew, color = '#8B0000', label = "X position")
# plt.plot(tNew, yNew, color = 'blue', label = "Y position")
# plt.plot(tNew, zNew, color = 'green', label = "Z position")

# #Plots velocity splines 
# plt.plot(tNew, dxNew, color = '#FF7276', label = "X velocity")
# plt.plot(tNew, dyNew, color = '#ADD8E6', label = "Y velocity")
# plt.plot(tNew, dzNew, color = '#90EE90', label = "Z velocity")
# plt.plot(distanceFromAllScatters(tNew), tNew, color = 'gray', label = "Distance From Scatterer")

# # Adds Labels
# plt.xlabel("Time")
# plt.ylabel("Position/Velocity")
# plt.legend()

# plt.show()