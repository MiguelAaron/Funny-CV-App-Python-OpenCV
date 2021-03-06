__author__ = 'ritchie'

from pyimage import imutils
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",
                help = "Path to the (optional) video file")
args = vars(ap.parse_args())

# Define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
# !---importance, these boundaries are in HSV color space, not RGB color space
lower = np.array([0,40,100],dtype='uint8')
upper = np.array([0,255,255],dtype='uint8')

# Detecting camera
if not args.get("video",False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

# Reading frame from our video
while True:
    (grabbed, frame) = camera.read()
    if args.get("video") and not grabbed:
        break

    frame = imutils.resize(frame, width=600)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted,lower,upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
    skinMask = cv2.erode(skinMask,kernel, iterations=2)
    skinMask = cv2.dilate(skinMask,kernel,iterations=2)

    skinMask = cv2.GaussianBlur(skinMask,(3,3),0)
    skin = cv2.bitwise_and(frame,frame,mask=skinMask)

    cv2.imshow("images",np.hstack([frame,skin]))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()





