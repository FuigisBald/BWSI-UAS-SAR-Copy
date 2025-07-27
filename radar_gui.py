import tkinter as tk
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
import pickle
import RTIPlot
import motion_capture_extraction

def radar_control_subprocess(
    node_id,
    scan_end,
    scan_resolution,
    BII,
    antenna_mode,
    transmit_gain,
    code_channel,
    persist_flag,
    slow_time_end,
    result_queue
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

    import paramiko


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
    local_json_path = os.path.abspath(f'./scans/{json_filename}')

    # Copy over json file from RPI
    sftp = client.open_sftp()
    sftp.get(rpi_json_path, local_json_path)
    sftp.close()
    result_queue.put({"json_path": local_json_path})
    print(f"Downloaded json file to {local_json_path}")

    # Close SSH
    client.close()
    print("SSH connection closed.")

def radar_control_starter(
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
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=radar_control_subprocess, args=(node_id, scan_end, scan_resolution, BII, antenna_mode, 
                                                                          transmit_gain, code_channel, persist_flag, slow_time_end, 
                                                                          result_queue))
    process.start()
    check_process_result(result_queue)

def check_process_result(result_queue):
    if result_queue.qsize() > 0:
        result = result_queue.get_nowait()  # Try getting result (non-blocking)
        if "json_path" in result:
            global local_json_path
            local_json_path = result["json_path"]
        else:
            root.after(500, lambda: check_process_result(result_queue))  # Try again in 0.5 sec
    else:
        root.after(500, lambda: check_process_result(result_queue))  # Try again in 0.5 sec

def draw_RTI():
    """
    Draws RTI based on json file and adds to GUI
    :param json_path: local path to json file
    """
    plt.close("all")
    global local_json_path
    if entry_json_path.get() != "":
        local_json_path = entry_json_path.get()
    pixel_polish_value = pixel_polish_bool.get()
    complex_value = complex_bool.get()

    fig, ax = plt.subplots()
    global scans, range_start, range_end, slow_times, db, extent
    scans, range_start, range_end, slow_times = RTIPlot.RTI(local_json_path, complex_value)
    extent = (0, range_end-range_start, slow_times[-1], slow_times[0])
    
    db = 20 * np.log10(np.abs(scans))

    if pixel_polish_value == 1:
        replicated_db = db
        min_threshold = 55
        max_threshold = 90
        replicated_db[replicated_db<min_threshold] = min_threshold
        replicated_db[replicated_db>max_threshold] = max_threshold
        db = replicated_db
    ax.imshow(
        db, aspect="auto", extent=extent, cmap="viridis"
    )

    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Slow Time (s)")
    cbar = fig.colorbar(ax.get_images()[0], ax=ax)
    cbar.set_label("Intensity (dB)")

    if entry_mocap_path.get() != "":
        mocap_path = entry_mocap_path.get()
        scatter_1_pos = list(map(float, entry_scatter_1.get().split(",")))
        scatter_2_pos = list(map(float, entry_scatter_2.get().split(",")))
        global t, mocap_plot_1, mocap_plot_2
        mocap_data, t = motion_capture_extraction.distancesFromScatters(mocap_path, [scatter_1_pos, scatter_2_pos])
        mocap_data = np.array(mocap_data)
        mocap_plot_1 = ax.plot(mocap_data[0] - 0.25, t, label = "Distance From Scatterer", color = 'red')[0]
        mocap_plot_2 = ax.plot(mocap_data[1] - 0.25, t, label = "Distance From Scatterer", color = 'red')[0]
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        global slow_time_slider
        slow_time_slider = tk.Scale(RTI_frame, from_=-t[-1]+extent[2], to=0, orient="vertical", resolution=0.1, command=update_RTI)
        slow_time_slider.grid(row=1, column=1, sticky='ns', pady=5)
        auto_time_align_btn = tk.Button(RTI_frame, text="Auto Align Slow Time", command=auto_time_align)
        auto_time_align_btn.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=RTI_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=5)

    pickle_output_btn = tk.Button(RTI_frame, text="Output to PKL", command=pickle_output)
    pickle_output_btn.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

def update_RTI(slow_time_offset):
    """
    Updates RTI extent based on slider value
    :param slow_time_offset: Slow time offset in seconds
    """ 
    plt.close("all")
    mocap_plot_1.set_ydata(t + float(slow_time_offset))
    mocap_plot_2.set_ydata(t + float(slow_time_offset))
    canvas.draw_idle()
    canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=5)

def auto_time_align():
    """
    Automatically aligns slow time for RTI
    """
    averages = []
    offsets = []
    mocap_plot_1.set_ydata(t)
    mocap_plot_2.set_ydata(t)
    for offset in range(0, ((-t[-1]+extent[2])*10).astype(int), -1):
        mocap_xy_1 = mocap_plot_1.get_xydata()
        mocap_xy_2 = mocap_plot_2.get_xydata()
        x_data_1, y_data_1 = mocap_xy_1[:, 0], mocap_xy_1[:, 1]
        x_data_2, y_data_2 = mocap_xy_2[:, 0], mocap_xy_2[:, 1]
        offset_y_data_1 = y_data_1 + offset/10
        offset_y_data_2 = y_data_2 + offset/10

        height = len(db)
        width = len(db[0])

        x_pix_1 = ((x_data_1 - extent[0]) / (extent[1] - extent[0]) * width).astype(int)
        y_pix_1 = ((extent[3] - offset_y_data_1) / (extent[3] - extent[2]) * height).astype(int)
        valid_indices_1 = (x_pix_1 >= 0) & (x_pix_1 < width) & (y_pix_1 >= 0) & (y_pix_1 < height)

        x_pix_2 = ((x_data_2 - extent[0]) / (extent[1] - extent[0]) * width).astype(int)
        y_pix_2 = ((extent[3] - offset_y_data_2) / (extent[3] - extent[2]) * height).astype(int)
        valid_indices_2 = (x_pix_2 >= 0) & (x_pix_2 < width) & (y_pix_2 >= 0) & (y_pix_2 < height)

        x_pix_1 = x_pix_1[valid_indices_1]
        y_pix_1 = y_pix_1[valid_indices_1]

        x_pix_2 = x_pix_2[valid_indices_2]
        y_pix_2 = y_pix_2[valid_indices_2]

        avg_1 = np.mean(db[y_pix_1, x_pix_1])
        avg_2 = np.mean(db[y_pix_2, x_pix_2])
        averages.append((avg_1+avg_2)/2)
        offsets.append(offset/10)
    max_avg_index = np.argmax(averages)
    slow_time_slider.set(offsets[max_avg_index])
    print(offsets[max_avg_index])

def pickle_output():
    """
    Outputs a pickle file for backprojection
    :param json_path: local path to json file
    :param positions: list of positions from mocap file
    """

    range_bins = np.linspace(0, range_end-range_start, len(scans[0])) + 0.25
    positions = motion_capture_extraction.intepolate_positions(slow_times, entry_mocap_path.get(), float(slow_time_slider.get()))

    output = {
        "scan_data": scans,
        "platform_pos": positions,
        "range_bins": range_bins
    }

    print(f"Outputed to pickleoutputs/{local_json_path[6:-5]}.pkl")
    with open(f"pickleoutputs/{local_json_path[6:-5]}.pkl", "wb") as f:
        pickle.dump(output, f)

    # Step 1: Get amplitude from json file
    # Step 2: Create range bins, starting at start_time and incrementing by 61ps (convert to meters)
    # Step 3: Interpolate slow time values for each scan 

def _quit():
    """ 
    Quits GUI
    """

    root.quit()
    root.destroy()

if __name__ == "__main__":
    main_font = ("Arial", 12)

    root = tk.Tk()
    root.title("RTI GUI")
    root.geometry("1180x630")

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

    # Create frame for buttons
    btn_frame = tk.Frame(config_frame, pady=10)
    btn_frame.grid(row=11, column=0, columnspan=2)

    # Button to fire radar based on config entry values
    fire_radar_btn = tk.Button(btn_frame, text="Fire Radar", font=main_font, command=lambda: radar_control_starter(
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
    fire_radar_btn.grid(row=11, column=0, padx=(50, 10), pady=10)

    # Button to display RTIRTI
    draw_rti_btn = tk.Button(btn_frame, text="Display RTI", font=main_font, command=draw_RTI)
    draw_rti_btn.grid(row=11, column=1, padx=(10, 50), pady=10)

    label_json_path = tk.Label(btn_frame, text="JSON Path:")
    label_json_path.grid(row=12, column=0, padx=5, pady=5)
    entry_json_path = tk.Entry(btn_frame, font=main_font, relief="raised")
    entry_json_path.grid(row=12, column=1, padx=10, pady=5)

    label_mocap_path = tk.Label(btn_frame, text="MoCap Path:")
    label_mocap_path.grid(row=13, column=0, padx=5, pady=5)
    entry_mocap_path = tk.Entry(btn_frame, font=main_font, relief="raised")
    entry_mocap_path.grid(row=13, column=1, padx=10, pady=5)

    label_scatter_1 = tk.Label(btn_frame, text="Scatterer 1 Position:")
    label_scatter_1.grid(row=14, column=0, padx=5, pady=5)
    entry_scatter_1 = tk.Entry(btn_frame, font=main_font, relief="raised")
    entry_scatter_1.grid(row=14, column=1, padx=10, pady=5)

    label_scatter_2 = tk.Label(btn_frame, text="Scatterer 2 Position:")
    label_scatter_2.grid(row=15, column=0, padx=5, pady=5)
    entry_scatter_2 = tk.Entry(btn_frame, font=main_font, relief="raised")
    entry_scatter_2.grid(row=15, column=1, padx=10, pady=5)

    label_pixel_polish = tk.Label(btn_frame, text="Pixel Polishing:")
    label_pixel_polish.grid(row=16, column=0, padx=5, pady=5)
    pixel_polish_bool = tk.IntVar(value=1)
    check_pixel_polish = tk.Checkbutton(btn_frame, variable=pixel_polish_bool, onvalue=1, offvalue=0)
    check_pixel_polish.grid(row=16, column=1, padx=10, pady=5)

    label_complex = tk.Label(btn_frame, text="Complex Data:")
    label_complex.grid(row=17, column=0, padx=5, pady=5)
    complex_bool = tk.IntVar(value=1)
    check_complex = tk.Checkbutton(btn_frame, variable=complex_bool, onvalue=1, offvalue=0)
    check_complex.grid(row=17, column=1, padx=10, pady=5)

    root.protocol("WM_DELETE_WINDOW", _quit)
    root.mainloop()
    