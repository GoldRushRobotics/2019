
# Packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time



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
    vs = cv2.VideoCapture(args["video"])

# Warm up
time.sleep(2.0)

while True:

  # Color frame
  frameColor = vs.read()

  # Gray frame
  frameGray = cv2.cvtColor(frameColor, cv2.COLOR_BGR2GRAY)

