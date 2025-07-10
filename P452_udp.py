import struct
import socket


def udp_request(
    mrm_ip_addr,  # MRM Info
    mrm_ip_port,  # MRM Info
    message_type,  # Mandatory parameters
    message_id,  # Mandatory parameters
    # Message specific parameters, default value of None to indicate if it has been set
    node_id=None,
    scan_start=None,
    scan_end=None,
    scan_resolution=None,
    BII=None,
    seg1_samples=None,
    seg2_samples=None,
    seg3_samples=None,
    seg4_samples=None,
    seg1_IM=None,
    seg2_IM=None,
    seg3_IM=None,
    seg4_IM=None,
    antenna_mode=None,
    transmit_gain=None,
    code_channel=None,
    persist_flag=None,
    scan_count=None,
    scan_interval_time=None,
    filter_mask=None,
    motion_filter=None,
    operational_mode=None,
    sleep_mode=None,
    reserved=None,
):
    """
    Sends a UDP request message to the specified MRM IP address and port.

    :param mrm_ip_addr: IP address of the MRM.
    :param mrm_ip_port: Port number of the MRM.
    :param message_type: Type of the message.
    :param message_id: Unique tracking identifier for the message.
    :param node_id: Antenna ID.
    :param scan_start: Start time for the scan (ps) relative to pulse transimition time.
    :param scan_end: End time for the scan (ps) relative to pulse transimition time.
    :param scan_resolution: Resolution of scan data (bins)
    :param BII: Log2 of the number of integrated samples.
    :param seg1_samples: Ignore
    :param seg2_samples: Ignore
    :param seg3_samples: Ignore
    :param seg4_samples: Ignore
    :param seg1_IM: Ignore
    :param seg2_IM: Ignore
    :param seg3_IM: Ignore
    :param seg4_IM: Ignore
    :param antenna_mode: Antenna mode (1: unknown, 2: unknown, 3: Transmit on A, Receive on B).
    :param transmit_gain: Transmit gain 0-63, 63 being max FCC power.
    :param code_channel: Coded UWB channel (0-10).
    :param persist_flag: Write config to FLASH memory? (0: no, 1: yes).
    :param scan_count: Number of scans to perform (0: Stop, 1: Single Shot, 2-65534: Number of scans, 65535: Forever).
    :param scan_interval_time: Time between scans (us) (0: As fast as possible).
    :param filter_mask: Specifies filter operation (1: Raw, 2: Bandpass, 3: Motion, 8: Detection list)
    :param motion_filter: Motion filter Index (0-3). See documentation for details.
    :param operational_mode: Operational mode (1: MRM).
    :param sleep_mode: Sleep mode (0: Active, 1: Idle, 2: Standby Ethernet, 3: Standby Serial, 4: Sleep).
    :param reserved: Reserved for future use (should be set to 0).
    """

    # Find used parameters and their format characters
    all_message_specific_params = [
        (node_id, "I"),  # (param, format_character)
        (scan_start, "i"),
        (scan_end, "i"),
        (scan_resolution, "H"),
        (BII, "H"),
        (seg1_samples, "H"),
        (seg2_samples, "H"),
        (seg3_samples, "H"),
        (seg4_samples, "H"),
        (seg1_IM, "B"),
        (seg2_IM, "B"),
        (seg3_IM, "B"),
        (seg4_IM, "B"),
        (antenna_mode, "B"),
        (transmit_gain, "B"),
        (code_channel, "B"),
        (persist_flag, "B"),
        (scan_count, "H"),
        (scan_interval_time, "I"),
        (filter_mask, "H"),
        (motion_filter, "B"),
        (operational_mode, "I"),
        (sleep_mode, "I"),
        (reserved, "H"),
    ]

    # Filter out unused paramters (if value is None, it has not been set)
    used_params = [message_type, message_id]
    format_string = "!HH"  # Base format for message type and ID
    for param, frmt in all_message_specific_params:
        if param is not None:
            used_params.append(param)
            format_string += frmt

    # Pack parameters
    packed_data = struct.pack(format_string, *used_params)

    # Send packed data
    try:
        sock.sendto(packed_data, (mrm_ip_addr, mrm_ip_port))
    except socket.error as err:
        print(f"Request socket error: {err}")


def udp_receive(buffer_size=4096):
    """
    Receives a UDP message from the specified MRM IP address and port.

    :param buffer_size: Size of the buffer to receive data.
    :return: Unpacked recieved data in a tuple, or None if an error occurs.
    :rtype: tuple or None
    """

    # List format strings for each message type
    message_types_formats = [
        (0x1101, "!HHI"),  # (message_type, format_string)
        (0x1102, "!HHIii6H8BII"),
        (0x1103, "!HHI"),
        (0x1104, "!HHI"),
        (0x1105, "!HHI"),
        (0x1106, "!HHI"),
        (0x1107, "!3HBBI"),
        (0xF101, "!HHBBHBBH4BI4Bi32sI"),
        (0xF102, "!HH"),
        (0xF103, "!HHII"),
        (0xF201, "!HH6Iiih4BHIHHi"),
        (0x1201, "!704H"),
        (0xF105, "!HHI"),
        (0xF106, "!HHII"),
        (0xF202, "!HH")
    ]

    try:
        data, addr = sock.recvfrom(buffer_size)
    except socket.error as err:
        print(f"Recieve socket error: {err}")
        return None

    # Determine message type
    message_type = struct.unpack("!H", data[0:2])[0]
    # Find the format string for the message type and unpack
    for msg_type, frmt in message_types_formats:
        if msg_type == message_type:
            try:
                unpacked_data = struct.unpack(frmt, data)
                return unpacked_data
            except struct.error as err:
                print(f"Unpacking error: {err}")
                return None


if __name__ == "__main__":
    host_ip_addr = "192.168.2.1"
    port = 21210
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host_ip_addr, port))

    udp_request(
        mrm_ip_addr="192.168.1.100",
        mrm_ip_port=21210,
        message_type=0x1005,
        message_id=1,
    )
    print(udp_receive())
