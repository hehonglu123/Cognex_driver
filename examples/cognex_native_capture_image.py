from RobotRaconteur.Client import *
from RobotRaconteurCompanion.Util.ImageUtil import ImageUtil
import cv2

url = 'rr+tcp://localhost:59901/?service=cognex'
# Connect to the object recognition sensor service
c = RRN.ConnectService(url)

img = c.cognex_capture_image()
img_util = ImageUtil(RRN, c)
mat = img_util.image_to_array(img)

cv2.imshow('image', mat)
cv2.waitKey()
