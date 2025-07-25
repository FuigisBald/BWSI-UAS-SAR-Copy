## UAS-SAR Code Team 1  
This is Team 1's code for the 2025 BWSI UAS-SAR course.  
*ALL FILES TO BE REVIEWED ARE IN MAIN*  
Branch Guide:   
    **main:** includes all completed working code  
        - **P452_udp.py:** code for communicating with the radar/raspberry pi  
        - **radar_control.py:** collecting radar data and getting it on local computer as a json file  
        - **radar_gui.py:** code for gui, allowing for user to fire radar and display rti plot  
        - **RTIPlot.py:** creates rti plots from json files  
        - **amplitude_graph.py:** creates an amplitude graph for a single radar scan  
        - **backprojection.py:** code to create backprojections from pickle files  
        - **motion_capture_extraction.py:** reads and plots motion capture data  
    **udp_dev:** used to develop code for communicating with radar/raspberry pi  
    **rti_dev:** used to write code to create a rti  
    **rpi_radar_dev:** used to collect data from the radar  
    **backprojection_dev:** used to create code for creating backprojections  
    **backprojection_optimization:** used to optimize backprojection code  
    **motioncapture_dev:** used to develop code to process motion capture data  
    **gui_dev:** used to develop code for visual interface to control firing radar and aligning mocap data with rti plot  
    **satellite_processing_dev:** used to develop code to generate a backprojection from satellite data