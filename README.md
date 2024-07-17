# Cognex Robot Raconteur Driver for In-Sight Devices

This package contains a Robot Raconteur driver for Cognex In-Sight Vision Systems. It has been tested
with an 7000 series device, but should work with other series as well. The driver works using the TCP/IP
communication feature that can be configured using the In-Sight software. The sensor initiates a connection
to the driver (reverse socket), and streams position information to the driver. The device must be configured
to use the correct ASCII string format.

The driver implements the [Robot Raconteur Standard Type](https://github.com/robotraconteur/robotraconteur_standard_robdef)
`com.robotraconteur.objectrecognition.ObjectRecognitionSensor`

See the `examples/` directory for example clients using the driver.

## Connection Info

The default connection information is as follows. These details may be changed using `--robotraconteur-*` command
line options when starting the service. Also see the
[Robot Raconteur Service Browser](https://github.com/robotraconteur/RobotRaconteur_ServiceBrowser) to detect
services on the network.

- URL: `rr+tcp://localhost:59901/?service=cognex`
- Device Name: `cognex_sensor`
- Node Name: `cognex_Service`
- ServiceName: `cognex`
- Root Object Type:
  - `com.robotraconteur.objectrecognition.ObjectRecognitionSensor`
  - `edu.robotraconteur.cognexsensor.CognexSensor`

## Installation

```bash
python -m pip install git+https://github.com/robotraconteur-contrib/cognex_robotraconteur_driver.git
```

Use `python3` on Linux if `python` is not aliased.

If using Conda, it is recommended to install the `robotraconteur` and `robotraconteur_companion_python` packages
using `conda install` before using `pip` to avoid potential pip/conda conflicts.

## Configure the Sensor

See [docs/cognex_setup](docs/cognex_setup.md) for instructions to configure the Cognex sensor.

## Running the Driver

Start the driver:

```bash
cognex-robotraconteur-driver --sensor-info-file=config/generic_cognex_sensor_default_config.yml
```

Optionally start using a module if the entrypoint does not work:

```bash
python -m cognex_robotraconteur_driver --sensor-info-file=config/generic_cognex_sensor_default_config.yml
```

The Cognex will attempt to connect to the driver and stream data. The `tools/socket_test.py` can be used
to view the raw data to make sure the sensor is communicating. Note the driver must be stopped before using
`tools/socket_test.py`

## Using the Service

See the `examples` directory for several examples using the driver. The following is a simple
example that will connect to the driver and print out the detected features.

```python
from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil

url = 'rr+tcp://localhost:59901/?service=cognex'

# Connect to the object recognition sensor service
c = RRN.ConnectService(url)

geom_util = GeometryUtil(RRN, c)

# Capture the currently recognized objects
recognized_objects = c.capture_recognized_objects()

# Print the recognized objects
for recognized_object in recognized_objects.recognized_objects:
    xyz, rpy = geom_util.pose_to_xyz_rpy(recognized_object.pose.pose.pose)
    print(f"object: {recognized_object.recognized_object.name} x: {xyz[0]:.3f}, y: {
            xyz[1]:.3f}, angle: {rpy[2]:.3f}, confidence: {recognized_object.confidence:.3f}")
```

## License

Apache 2.0 Licensed by Rensselaer Polytechnic Institute and Wason Technology, LLC

Author: Honglu He and John Wason

## Acknowledgment

This work was supported in part bythe Advanced Robotics for Manufacturing ("ARM") Institute under Agreement Number W911NF-17-3-0004 sponsored by the Office of the Secretary of Defense. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of either ARM or the Office of the Secretary of Defense of the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes, notwithstanding any copyright notation herein.

This work was supported in part by the New York State Empire State Development Division of Science, Technology and Innovation (NYSTAR) under contract C160142.

![](https://github.com/robotraconteur/robotraconteur/blob/master/docs/figures/arm_logo.jpg?raw=true)
![](https://github.com/robotraconteur/robotraconteur/blob/master/docs/figures/nys_logo.jpg?raw=true)
