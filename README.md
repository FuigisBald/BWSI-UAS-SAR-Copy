UAS-SAR Code Team 1
This is Team 1's code for the 2025 BWSI UAS-SAR course. 
Branch Guide:
    main:
        -ALL FILES TO BE REVIEWED ARE IN MAIN
        -includes all completed working code
        - P452_udp.py:
            - code for communicating with the radar/raspberry pi
        - radar_control.py:
            - collecting radar data and getting it on local computer as a json file
        -RTIPlot.py:
            - creates rti plots from json files
        - amplitude_graph.py:
            -creates an amplitude graph for a single radar scan
        - backprojection.py:
            - code to create backprojections from pickle files 
        -motioncaptureExtraction.py:
            - reads and plots motion capture data

    udp_dev: used to develop code for communicating with radar/raspberry pi
    rti_dev: used to write code to create a rti
    rpi_radar_dev: used to collect data from the radar
    backprojection_dev: used to create code for creating backprojections
    backprojection_optimization: used to optimize backprojection code
    motioncapture_dev: used to develop code to process motion capture data
    gui_dev: used to develop code for visual interface
    
    
