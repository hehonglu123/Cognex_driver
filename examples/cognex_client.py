from RobotRaconteur.Client import *
import sys
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil

def main():

    url = 'rr+tcp://localhost:59901/?service=cognex'
    if (len(sys.argv) >= 2):
        url = sys.argv[1]

    # Connect to the object recognition sensor service
    c = RRN.ConnectService(url)

    geom_util = GeometryUtil(RRN, c)

    # Capture the currently recognized objects
    recognized_objects = c.capture_recognized_objects()

    # Print the recognized objects
    for recognized_object in recognized_objects.recognized_objects:
        xyz, rpy = geom_util.pose_to_xyz_rpy(recognized_object.pose.pose.pose)
        print(f"object: {recognized_object.recognized_object.name} x: {xyz[0]:.3f}, y: {xyz[1]:.3f}, angle: {rpy[2]:.3f}, confidence: {recognized_object.confidence:.3f}")


if __name__ == '__main__':
    main()
