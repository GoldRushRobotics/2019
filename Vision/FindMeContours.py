
# Packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2 as cv
import imutils
import time
import numpy as np



# Video setup
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# Grab video

if not args.get("video", False):
    vs = VideoStream(src=1).start()

# otherwise, grab a reference to the video file
else:
    vs = cv.VideoCapture(args["video"])

# Warm up
time.sleep(2.0)

while True:

  # Color frame
  frameColor = vs.read()

  # Gray frame
  frameGray = cv.cvtColor(frameColor, cv.COLOR_BGR2GRAY)

  # thresh = cv.inRange(frameGray, 127, 255, 0)

  edges = cv.Canny(frameGray,127,255)
  # contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

  # cnt = contours[0]
  # cv.drawContours(frameColor, [cnt], 0, (0,255,0), 3)
  cv2.imshow('frame',frameGray)
  if cv.waitKey(1) & 0xFF == ord('q'):
    break
