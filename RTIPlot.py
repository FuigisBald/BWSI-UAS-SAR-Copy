import matplotlib.pyplot as plt
import numpy as np
import json

def RTI(json_path):
    """
    Draws an RTI using radar data from json file.
    :param json_path: local path to json file
    """
    # Pulls data from json file
    with open(json_path, "r") as f:
        received_data = json.load(f)

    # Gets the scan start and end times
    scan_start = received_data["scan_start"]
    scan_end = received_data["scan_end"]

    scans = []
    slow_time = []

    # loops through all the scans 
    for scan in received_data["scans"]:
        slow_time.append(scan[0])
    range_start = scan_start * 299792458 * (10e-13) / 2
    range_end = scan_end * 299792458 * (10e-13) / 2

    # Converts the amplitude array into decibels
    db = 20 * np.log10(np.abs(scans))

    fig, ax = plt.subplots()

    img = ax.imshow(
        db, aspect="auto", extent=(0, range_end-range_start, slow_time[-1], slow_time[0]), cmap="viridis"
    )

    ax.set_title("RTI")
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Slow Time (s)")

    # Add colorbar and label
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label("Intensity (dB)")

    return img

# Plots the data
if __name__ == "__main__":
    img = RTI("C:/Users/thema/Downloads/scans-2025-07-12_04-44-43.json")
    plt.imshow(img.get_array(), cmap=img.get_cmap(), aspect="auto", extent=img.get_extent())
    plt.title("RTI")
    plt.xlabel("Range (m)")
    plt.ylabel("Slow Time (s)")
    plt.show()