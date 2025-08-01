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
        # Check if packets were dropped, and set to zeros
        if len(scan[1]) != sample_count:
            scan[1] = [0] * sample_count
        
        slow_time.append(scan[0])
        scans.append(scan[1])

    range_start = scan_start * 299792458 * (1e-12) / 2 # Converts to meters
    range_end = scan_end * 299792458 * (1e-12) / 2 # Converts to meters

    if complex_data == 1:
        # Runs hilbert transform on scan data to get complex data
        hilbert_data = hilbert(scans)
        nphilbert_data = np.array(hilbert_data)
        return nphilbert_data, range_start, range_end, slow_time
    else:
        return scans, range_start, range_end, slow_time