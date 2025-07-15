import P452_udp
import time
import json


mrm_ip_addr = "192.168.1.100"
port = 21210
message_id = 2 # Message ID is originally 2 to account for the 2 setup messages.

def setup(
    node_id,
    scan_end,
    scan_resolution,
    BII,
    antenna_mode,
    transmit_gain,
    code_channel,
    persist_flag,
    scan_start=20014, #3m offset,

):
    """
    Sets and gets config request from P452 Radar to initiate.
    :param mrm_ip_addr: IP address of the MRM.
    :param mrm_ip_port: Port number of the MRM.
    :param message_type: Type of the message.
    :param message_id: Unique tracking identifier for the message.
    :param node_id: Antenna ID.
    :param scan_start: Start time for the scan (ps) relative to pulse transimition time.
    :param scan_end: End time for the scan (ps) relative to pulse transimition time.
    :param scan_resolution: Resolution of scan data (bins)
    :param BII: Log2 of the number of integrated samples.
    :param antenna_mode: Antenna mode (1: unknown, 2: unknown, 3: Transmit on A, Receive on B).
    :param transmit_gain: Transmit gain 0-63, 63 being max FCC power.
    :param code_channel: Coded UWB channel (0-10).
    :param persist_flag: Write config to FLASH memory? (0: no, 1: yes).
    """

    # Convert scan_end from m to ps
    scan_end = int(scan_end * 2 * 1e12 / 299792458)

    P452_udp.udp_request(
        mrm_ip_addr=mrm_ip_addr,
        mrm_ip_port=port,
        message_type=0x1001, # Set config request message
        message_id=0,
        node_id=node_id,
        scan_start=scan_start,
        scan_end=scan_end,
        scan_resolution=scan_resolution,
        BII=BII,
        seg1_samples=0,
        seg2_samples=0,
        seg3_samples=0,
        seg4_samples=0,
        seg1_IM=0,
        seg2_IM=0,
        seg3_IM=0,
        seg4_IM=0,
        antenna_mode=antenna_mode,
        transmit_gain=transmit_gain,
        code_channel=code_channel,
        persist_flag=persist_flag,
    )

    set_config_confirm = P452_udp.udp_receive()
    if set_config_confirm[-1] != 0:
        print(f"Error status recieved when setting configuration, see response: {set_config_confirm}")
        return
    else:
        print(set_config_confirm)

    P452_udp.udp_request(
        mrm_ip_addr=mrm_ip_addr,
        mrm_ip_port=port,
        message_type=0x1002, # Get config request message
        message_id=1,
    )

    get_config_confirm = P452_udp.udp_receive()
    if get_config_confirm[-1] != 0:
        print(f"Error status recieved when getting configuration, see response: {get_config_confirm}")
        return
    else:
        print(get_config_confirm)
        return get_config_confirm[3], get_config_confirm[4] # Scan start and end times in ps

def radar_control(
        scan_start,
        scan_end,
        message_id, 
        scan_count,
        scan_interval
):
    """
    Requests control of the radar to start scanning.

    :param message_id: Unique tracking identifier for the message.
    :param scan_count: Number of scans to perform.
    :param scan_interval: Time between scans in microseconds.
    :return: List of scan data amplitudes.
    :rtype: list[int]
    """

    P452_udp.udp_request(
        mrm_ip_addr=mrm_ip_addr,
        mrm_ip_port=port,
        message_type=0x1003, # Control request message
        message_id=message_id,
        scan_count=scan_count,
        reserved=0,
        scan_interval_time=scan_interval
    )

    control_confirm = P452_udp.udp_receive()
    if control_confirm[-1] != 0:
        print(f"Error status recieved when requesting control, see response: {control_confirm}")
        return
    else:
        print("Requested radar control successfully.")

    scans = []
    scans_start_time = time.time()

    for scan_n in range(scan_count):
        scan_end_time = time.time()
        message_index = 0
        total_messages = 2 # Placeholder to enter while loop
        amplitudes = []

        while message_index + 1 < total_messages:
            scan_info = P452_udp.udp_receive()
            message_index = scan_info[17]
            total_messages = scan_info[18]
            scan_data = scan_info[19:19+scan_info[15]]
            amplitudes.extend(scan_data)


        scan_time = round(scan_end_time - scans_start_time, 5)
        scans.append((scan_time, amplitudes))

    datetime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())

    json_data = {
        "scan_start": scan_start,
        "scan_end": scan_end,
        "scans": scans
    }

    with open(f"scans-{datetime}.json", "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    scan_start, scan_end = setup(
        node_id=2,
        scan_end=15, # Max range in m
        scan_resolution=32,
        BII=9,
        antenna_mode=3,
        transmit_gain=63,
        code_channel=1,
        persist_flag=0,
    )
    radar_control(scan_start=scan_start, scan_end=scan_end, message_id=message_id, scan_count=1000, scan_interval=4000)