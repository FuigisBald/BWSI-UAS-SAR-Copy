import matplotlib.pyplot as plt
import numpy as np
import json

# Pulls data from json file
with open("scans-2025-07-11_18-42-43.json", "r") as f:
    received_data = json.load(f)

# Gets the scan start and end times
scan_start = received_data["scan_start"]
scan_end = received_data["scan_end"]

scans = []
long_time = []

for i, scan in enumerate(received_data["scans"]):
    amplitudes = []
    for j, amplitude in enumerate(scan[1]):
        range = (j*61 + scan_start) * 299792458 * (10e-13) / 2  # Convert time (ps) to range (m)
        amplitudes.append(amplitude)
    scans.append(amplitudes)
    long_time.append(scan[0])

range_start = scan_start * 299792458 * (10e-13) / 2
range_end = scan_end * 299792458 * (10e-13) / 2

#Converts the amplitude array into decibels
db = 20 * np.log10(np.abs(scans))

# Plots the data
plt.imshow(
    db, aspect="auto", extent=(range_start, range_end, long_time[-1], long_time[0]),
)
plt.colorbar()
plt.show()
