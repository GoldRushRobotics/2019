import time
import cv2
from FindMyHome import home

if __name__ == "__main__":
    capture = cv2.VideoCapture(1)

    w = int(capture.get(3))
    h = int(capture.get(4))

    time.sleep(2)

    while 1:
        ret, firstFrame = capture.read()

        # Calculate the home color from the first frame
        homeColor = home(firstFrame, w, h)

        print("h{0}".format(homeColor))
