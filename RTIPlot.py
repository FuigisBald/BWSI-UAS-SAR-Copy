import numpy as np
import json
from scipy.signal import hilbert

def RTI(json_path, complex_data):
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
    for i, scan in enumerate(received_data["scans"]):
        sample_count = len(received_data["scans"][0][1])
        if len(scan[1]) > sample_count:
            extra_data = scan[1][sample_count:]
            scan[1] = scan[1][:sample_count]
            scans[i-1].extend(extra_data)
        slow_time.append(scan[0])
        scans.append(scan[1])

    range_start = scan_start * 299792458 * (1e-12) / 2 # Converts to meters
    range_end = scan_end * 299792458 * (1e-12) / 2 # Converts to meters

    if complex_data == 1:
        hilbert_data = hilbert(scans)
        nphilbert_data = np.array(hilbert_data)
        rotshiftedHilbert_data = []
        for i in range(len(hilbert_data[0])):
            rotshiftedHilbert_data.append(nphilbert_data[:, i]*np.exp(-4j * np.pi * i*61*(1e-12) * 4.3 / 299792458))
        
        shiftedHilbert_data = np.swapaxes(rotshiftedHilbert_data, 0, 1)

        # Converts the amplitude array into decibels
        return shiftedHilbert_data, range_start, range_end, slow_time
    else:
        return scans, range_start, range_end, slow_time
    
# # Plots the data
# if __name__ == "__main__":
#     img = RTI("path")
#     plt.imshow(img.get_array(), cmap=img.get_cmap(), aspect="auto", extent=img.get_extent())
#     plt.title("RTI")
#     plt.xlabel("Range (m)")
#     plt.ylabel("Slow Time (s)")
#     plt.show()