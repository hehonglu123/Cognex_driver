from RobotRaconteur.Client import *
import sys
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil

geom_util = None

def new_frame(pipe_ep):

    global geom_util

    latest = None
    while (pipe_ep.Available > 0):
        latest = pipe_ep.ReceivePacket()

    if latest is None:
        return
    
    for recognized_object in latest.recognized_objects.recognized_objects:
        xyz, rpy = geom_util.pose_to_xyz_rpy(recognized_object.pose.pose.pose)
        print(f"object: {recognized_object.recognized_object.name} x: {xyz[0]:.3f}, y: {xyz[1]:.3f}, angle: {rpy[2]:.3f}, confidence: {recognized_object.confidence:.3f}")

    if len(latest.recognized_objects.recognized_objects) == 0:
        print("No objects detected")

def main():

    url = 'rr+tcp://localhost:59901/?service=cognex'
    if (len(sys.argv) >= 2):
        url = sys.argv[1]

    # Connect to the object recognition sensor service
    c = RRN.ConnectService(url)

    global geom_util
    geom_util = GeometryUtil(RRN, c)

    # Connect to the object recognition sensor pipe
    p = c.object_recognition_sensor_data.Connect(-1)

    # Add the packet received event
    p.PacketReceivedEvent += new_frame

    input("press enter to quit")

if __name__ == '__main__':
    main()
