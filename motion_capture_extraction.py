import numpy as np
from scipy.interpolate import UnivariateSpline
import pandas as pd

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
    """
    Calculates the distance between each scatterer and the motion capture data.
    :param csv: local path to csv file
    :param scatterersPos: 3D positions of each scatterer
    :return: 2D array of distances, and the time array
    """
    df = pd.read_csv(csv, skiprows = 6, usecols=[1, 6, 7, 8])

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

    tNew = np.linspace(min(t), max(t), numEstimates)

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
    """
    Interpolates radar scan times into motion capture position data.
    :param slow_times: 1D array of slow times in seconds
    :param mocap_path: local path to csv file
    :param offset: time offset in seconds
    :return: 2D array of positions with each row being [x, y, z]
    """
    df = pd.read_csv(mocap_path, skiprows = 6, usecols=[1, 6, 7, 8])

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