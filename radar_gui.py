import tkinter as tk
import ctypes
import paramiko
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
import RTIPlot

# Connect to Raspberry Pi with SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Get Raspberry Pi information from file
with open("rpi_information.txt", "r") as f:
    rpi_info = f.read().split()

try:
    client.connect(rpi_info[0], username=rpi_info[1], password=rpi_info[2])
    print("Successfully connected via SSH.")
except paramiko.AuthenticationException:
    print("Authentication failed. Check username and password.")
except paramiko.SSHException as e:
    print(f"SSH connection error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

if platform.system() == "win32":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

main_font = ("Arial", 12)

root = tk.Tk()
root.title("RTI GUI")
root.geometry("1180x700")

# TKinter elements
config_frame = tk.Frame(root, borderwidth=2, relief="groove") # Setup frame for config
config_frame.pack(side='left', fill='both', expand=False, padx=5, pady=5)

config_title = tk.Label(config_frame, text="Config Settings", font=("Arial", 16)) # Config title
config_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Add labels and entry fields for all config settings
label_node_id = tk.Label(config_frame, text="Node ID:")
label_node_id.grid(row=1, column=0, padx=5, pady=5)
entry_node_id = tk.Entry(config_frame, font=main_font, relief="raised")
entry_node_id.grid(row=1, column=1, padx=10, pady=5)
entry_node_id.insert(0, "2")

label_scan_end = tk.Label(config_frame, text="Scan End (m):")
label_scan_end.grid(row=2, column=0, padx=5, pady=5)
entry_scan_end = tk.Entry(config_frame, font=main_font, relief="raised")
entry_scan_end.grid(row=2, column=1, padx=10, pady=5)
entry_scan_end.insert(0, "15")

label_scan_res = tk.Label(config_frame, text="Scan Resolution:")
label_scan_res.grid(row=3, column=0, padx=5, pady=5)
entry_scan_res = tk.Entry(config_frame, font=main_font, relief="raised")
entry_scan_res.grid(row=3, column=1, padx=10, pady=5)
entry_scan_res.insert(0, "32")

label_BII = tk.Label(config_frame, text="BII:")
label_BII.grid(row=4, column=0, padx=5, pady=5)
entry_BII = tk.Entry(config_frame, font=main_font, relief="raised")
entry_BII.grid(row=4, column=1, padx=10, pady=5)
entry_BII.insert(0, "9")

label_antenna_mode = tk.Label(config_frame, text="Antenna Mode:")
label_antenna_mode.grid(row=5, column=0, padx=5, pady=5)
entry_antenna_mode = tk.Entry(config_frame, font=main_font, relief="raised")
entry_antenna_mode.grid(row=5, column=1, padx=10, pady=5)
entry_antenna_mode.insert(0, "3")

label_transmit_gain = tk.Label(config_frame, text="Transmit Gain:")
label_transmit_gain.grid(row=6, column=0, padx=5, pady=5)
entry_transmit_gain = tk.Entry(config_frame, font=main_font, relief="raised")
entry_transmit_gain.grid(row=6, column=1, padx=10, pady=5)
entry_transmit_gain.insert(0, "63")

label_code_channel = tk.Label(config_frame, text="Code Channel:")
label_code_channel.grid(row=7, column=0, padx=5, pady=5)
entry_code_channel = tk.Entry(config_frame, font=main_font, relief="raised")
entry_code_channel.grid(row=7, column=1, padx=10, pady=5)
entry_code_channel.insert(0, "1")

label_persist_flag = tk.Label(config_frame, text="Persist Flag:")
label_persist_flag.grid(row=8, column=0, padx=5, pady=5)
entry_persist_flag = tk.Entry(config_frame, font=main_font, relief="raised")
entry_persist_flag.grid(row=8, column=1, padx=10, pady=5)
entry_persist_flag.insert(0, "0")

label_slow_time_end = tk.Label(config_frame, text="Slow Time End:")
label_slow_time_end.grid(row=9, column=0, padx=5, pady=5)
entry_slow_time_end = tk.Entry(config_frame, font=main_font, relief="raised")
entry_slow_time_end.grid(row=9, column=1, padx=10, pady=5)
entry_slow_time_end.insert(0, "5")

# Create frame to display RTI
RTI_frame = tk.Frame(root, borderwidth=2, relief="groove")
RTI_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
RTI_title = tk.Label(RTI_frame, text="RTI", font=("Arial", 16))
RTI_title.grid(row=0, column=0, sticky='ew')
RTI_frame.grid_columnconfigure(0, weight=1)

def radar_control(
    node_id,
    scan_end,
    scan_resolution,
    BII,
    antenna_mode,
    transmit_gain,
    code_channel,
    persist_flag,
    slow_time_end
):
    """
    Requests radar control from the Raspberry Pi through SSH.
    :param node_id: Node ID of the radar
    :param scan_end: Scan end distance in meters
    :param scan_resolution: Scan resolution in bins
    :param BII: Log2 of the number of integrated samples
    :param antenna_mode: Antenna mode (1: unknown, 2: unknown, 3: Transmit on A, Receive on B)
    :param transmit_gain: Transmit gain 0-63, 63 being max FCC power
    :param code_channel: Coded UWB channel (0-10)
    :param persist_flag: Write config to FLASH memory? (0: no, 1: yes)
    :param slow_time_end: End slow time of RTI (s)
    """

    global local_json_path
    print("Requesting radar control")
    stdin, stdout, stderr = client.exec_command(f"python Desktop/UASSAR-1/radar_control.py --node_id {node_id} --scan_end {scan_end}" \
    f" --scan_resolution {scan_resolution} --BII {BII} --antenna_mode {antenna_mode} --transmit_gain {transmit_gain}" \
    f" --code_channel {code_channel} --persist_flag {persist_flag} --slow_time_end {slow_time_end}") # Run command through SSH

    errors = stderr.read().decode()
    if errors:
        print(f"Error: {errors}")

    print("Getting json file from Raspberry Pi")
    json_filename = stdout.read().decode()[:-1]
    rpi_json_path = f"/home/sardemo/Desktop/UASSAR-1/{json_filename}"
    local_json_path = f"filepath/{json_filename}"

    # Copy over json file from RPI
    sftp = client.open_sftp()
    sftp.get(rpi_json_path, local_json_path)
    sftp.close()
    print(f"Downloaded json file to {local_json_path}")

def draw_RTI(json_path):
    """
    Draws RTI based on json file and adds to GU
    :param json_path: local path to json file
    """

    fig, ax = plt.subplots()
    img = RTIPlot.RTI(json_path)
    ax.imshow(img.get_array(), cmap=img.get_cmap(), aspect="auto", extent=img.get_extent())
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Slow Time (s)")
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label("Intensity (dB)")

    # ax.plot([1,4], [0.06,5], color="red", linestyle="--")

    canvas = FigureCanvasTkAgg(fig, master=RTI_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=5)

def _quit():
    """
    Quits GUI
    """

    root.quit()
    root.destroy()

# Create frame for buttons
btn_frame = tk.Frame(config_frame, pady=10)
btn_frame.grid(row=11, column=0, columnspan=2)

# Button to fire radar based on config entry values
fire_radar_btn = tk.Button(btn_frame, text="Fire Radar", font=main_font, command=lambda: radar_control(
    node_id=int(entry_node_id.get()),
    scan_end=int(entry_scan_end.get()),
    scan_resolution=int(entry_scan_res.get()),
    BII=int(entry_BII.get()),
    antenna_mode=int(entry_antenna_mode.get()),
    transmit_gain=int(entry_transmit_gain.get()),
    code_channel=int(entry_code_channel.get()),
    persist_flag=int(entry_persist_flag.get()),
    slow_time_end=int(entry_slow_time_end.get())
    )
)
fire_radar_btn.grid(row=11, column=0, padx=10)

# Button to display RTI
draw_rti_btn = tk.Button(btn_frame, text="Display RTI", font=main_font, command=lambda: draw_RTI(local_json_path))
draw_rti_btn.grid(row=11, column=1, padx=10)

root.protocol("WM_DELETE_WINDOW", _quit)
root.mainloop()

# Close SSH
client.close()
print("SSH connection closed.")