import json
import matplotlib.pyplot as plt

#Pulls data from json file
with open('scans-2025-07-11_17-11-48.json', 'r') as f:
    receivedData = json.load(f)

#Sample data from deepseek transformed into how we will actually be receiving the data
receivedAmplitude = []
ranges = []

scan_start = receivedData["scan_start"]

for i, amplitude in enumerate(receivedData["scans"][0][1]):
    time = i*61 + scan_start
    range = time * 299792458 * (10e-13) / 2  # Convert time to range in meters
    ranges.append(range)
    receivedAmplitude.append(amplitude * range**4)

# Plot amplitude vs time
plt.figure(figsize=(10, 6))
plt.plot(ranges, receivedAmplitude, label='Amplitude')
plt.title('Amplitude vs Range')
plt.xlabel('Range (m)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()