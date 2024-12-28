# Cognex Robot Raconteur Driver for In-Sight Devices

This package contains a Robot Raconteur driver for Cognex In-Sight Vision Systems. It has been tested
with an 7000 series device, but should work with other series as well. The driver works using the TCP/IP
communication feature that can be configured using the In-Sight software. The device must be configured
to use the correct ASCII string format.

The driver implements the [Robot Raconteur Standard Type](https://github.com/robotraconteur/robotraconteur_standard_robdef)
`com.robotraconteur.objectrecognition.ObjectRecognitionSensor`. This driver also adds functions specific to
the Cognex device.

This version of the driver uses the Cognex as a TCP/IP server and the driver acting as TCP client. This
is different than older versions of the driver that use a "reverse socket", where the Cognex device is a TCP
client, and the driver is a TCP server. See the setup instructions to make this adjustment.

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

The Cognex sensor can be configured using either the Easy Builder or Spreadsheet programming interface. See
the following documents for instructions in the `docs/` directory:

- [Easy Builder Setup](docs/cognex_setup.md)
- [Spreadsheet Setup](docs/cognex_setup_spreadsheet.md)

## Running the Driver

Start the driver:

```bash
cognex-robotraconteur-driver --sensor-info-file=config/generic_cognex_sensor_default_config.yml --cognex-host=192.168.1.175
```

Optionally start using a module if the entrypoint does not work:

```bash
python -m cognex_robotraconteur_driver --sensor-info-file=config/generic_cognex_sensor_default_config.yml --cognex-host=192.168.1.175
```

Replace `192.168.1.175` with the address of the Cognex device. Use the Cognex software to read the IP address
of the device and optionally assign a static IP address. It is recommended that the DHCP server be used to assign
a static IP address by making an entry in the DHCP server pre-assigned address table. This is a common
feature available in commercial cable routers and open-source router software like OpenWRT and PFSense.

## Command Line Options

- `--sensor-info-file=` - (required) The sensor info file. Info files are available in the `config/` directory. See the [object sensor info file documentation](https://github.com/robotraconteur/robotraconteur_standard_robdef/blob/master/docs/info_files/objectrecognition.md).
- `--cognex-host=` - (required) The IP address or hostname of the Cognex sensor. Use the Cognex software to find and configure the sensor IP address.
- `--cognex-port=` - The port that the Cognex is listening for connections. Default is port 3000.
- `--cognex-password=` - The password for the Cognex native mode. By default the password is set to empty on the device. This is only used for the native commands in the next section.

All Robot Raconteur node setup command line options are supported. See [Robot Raconteur Node Command Line Options](https://github.com/robotraconteur/robotraconteur/wiki/Command-Line-Options)

## Cognex Native Mode Commands

This driver uses root object type `edu.robotraconteur.cognexsensor.CognexSensor`. This type
extends the standard type `com.robotraconteur.objectrecognition.ObjectRecognitionSensor`, and adds several functions
that are specific to the Cognex sensor. These functions use the ["Native Mode Communications"](https://support.cognex.com/docs/is_613/web/EN/ise/Content/Communications_Reference/NativeModeCommunications.htm) which is an ASCII telnet protocol. These functions are
very slow, and should be used sparingly. This driver mainly uses the TCP/IP communication protocol that
is configured using the Easy Builder or Spreadsheet programming interface for real-time communication.

- `function string cognex_get_cell(string cell)`

  Get the value of a cell in the spreadsheet. Uses native mode command [`GV`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/GetValue_Spreadsheet.htm)
  - `cell`: The cell to read value. Must have form `G005`, `B015`, etc.
  - Returns: The value of the cell as a string
- `function void cognex_set_cell_int(string cell, int32 value)`

  Set the value of a cell to an integer. Cell must be type [EditInt()](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Reference/EditInt.htm). Uses native mode command [`SI`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/SetInteger_Spreadsheet.htm)
  - `cell`: The cell to read value. Must have form `G005`, `B015`, etc.
  - `value`: The new cell value.
- `function void cognex_set_cell_float(string cell, double value)`

  Set the value of a cell to a float. Cell must be type [EditFloat()](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Reference/EditFloat.htm).Uses native mode command [`SF`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/SetFloat_Spreadsheet.htm)
  - `cell`: The cell to read value. Must have form `G005`, `B015`, etc.
  - `value`: The new cell value.
- `function void cognex_set_cell_string(string cell, string value)`

  Set the value of a cell to a string. Cell must be type [EditString()](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Reference/EditString.htm).Uses native mode command [`SS`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/SetString_Spreadsheet.htm)
  - `cell`: The cell to read value. Must have form `G005`, `B015`, etc.
  - `value`: The new cell value.
- `function void cognex_trigger_acquisition()`

  Trigger acquisition of a new frame. Image acquisition must be set to "External". Uses native mode command [`SW8`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/SetEventAndWait.htm)
- `function void cognex_trigger_event(int32 evt_num)`

  Trigger an event. Uses native mode command [`SW`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/SetEventAndWait.htm)
  - `evt_num`: An event number between 0 and 8.
- `function Image cognex_capture_image()`

  Captures an RGB or mono image from the cognex device and returns a standard Robot Raconteur image. This function
  is very slow, and should only be used sparingly. Uses native mode command [`RB`](https://support.cognex.com/docs/is_574/web/EN/ise/Content/Communications_Reference/ReadBMP.htm)

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
