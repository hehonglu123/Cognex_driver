# Cognex Object Detection with RR Service

## Cognex Object Detection Setup with In-Sight Explorer

### Cognex Connection
Under `Add Sensor/Device to Network`, Cognex camera should appear with its IP address, make sure computer is set to DHCP.
<img src="images/IP_lookup.png" alt="Alt Text" width="500" height="auto">

### Object Training
Follow Cognex instruction to create pattern for object detection.
<img src="images/sample_pattern.png" alt="Alt Text" width="800" height="auto">

### Continuous Detection
Make Cognex camera trigger in Continuous mode, adjust image parameters according to the environment.

<img src="images/image_setup.png" alt="Alt Text" width="500" height="auto">

<img src="images/setup_final.png" alt="Alt Text" width="500" height="auto">

### Communication Setup
Under `Communications`->`TCP/IP`, set up IP of the PC as `Server Host Name` as shown in 
<img src="images/communication.png" alt="Alt Text" width="500" height="auto">

To format the message, go to `Format Output String` -> `Format String...`, and follow the same structure as shown in image below for every object. Notice maximum output string length is 255.
<img src="images/string_format.png" alt="Alt Text" width="400" height="auto">

## RR Service for Cognex
`Cognex_objdet.py` provides an RR service wrapper for a socket connection with Cognex camera directly. This is highly customized from `final_with_no_objects.job` loaded in Cognex to parse the formatted string into pose data.

