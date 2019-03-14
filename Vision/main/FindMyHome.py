'''

This function is called at the beginning of main to determine what color/position our home is. Basically a big boi setup script.

'''


# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time

def home(image, width, height):
    # cap = cv2.VideoCapture(0)
    # #height = cap.get(4)
    #
    # if cap.isOpened():
    #     ret, frame = cap.read()
    # else:
    #     ret = False
    actColor = ' '
    H_Upper = 225
    H_Lower = 350
    W_Upper = 400
    W_Lower = 250

    cropped = image[H_Upper:H_Lower, W_Lower:W_Upper] #img[height_range, width_range]
    cv2.imshow("cropped", cropped)

    # # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-v", "--video",
    #             help="path to the (optional) video file")
    # ap.add_argument("-b", "--buffer", type=int, default=64,
    #             help="max buffer size")
    # args = vars(ap.parse_args())

    #       lower bound , upper bound
    b = ([102, 0, 0], [255, 204, 204])
    g = ([0, 0, 0], [75, 255, 75])
    y = ([0, 160, 170], [220, 255, 255])
    r = ([0, 0, 118], [194, 194, 255])

    #pts = deque(maxlen=args["buffer"])

    totalPix = (0, 0, 0)

    for h in range(0, 149):
        for w in range(0, 124):
            totalPix = totalPix + cropped[w][h]

    avgPix = totalPix / 18750

    avgFrame = cv2.rectangle(cropped,(72,0),(0,60),avgPix,50)

    cv2.imshow("AVG Color", avgFrame)
    pix = [avgPix[0], avgPix[1], avgPix[2]]

    col = []
    colors = ['r', 'g', 'b', 'y']

    for color in (r, g, b, y):
        low, up = color
        isCol = True
        for i, x in enumerate(pix):
            if low[i] < x < up[i]:
                isCol &= True
            else:
                isCol &= False

        col.append(isCol)

    for value in range(4):
        if col[value] == True:
            actColor = colors[value]
            break

    return actColor



    # if not args.get("video", False):
    #     vs = VideoStream(src=0).start()
    #
    # # otherwise, grab a reference to the video file
    # else:
    #     vs = cv2.VideoCapture(args["video"])
    #
    # #allow the camera or video file to warm upper
    # time.sleep(2.0)
    #
    # #keep looping
    # while True:
    #     # grab the current frame
    #     frame = vs.read()
    #
    #     # handle the frame from VideoCapture or VideoStream
    #     frame = frame[1] if args.get("video", False) else frame
    #
    #     # if we are viewing a video and we did not grab a frame,
    #     # then we have reached the end of the video
    #     if frame is None:
    #         break
    #
    #     # if the 'q' key is pressed, stop the loop
    #     if (cv2.waitKey(1) & 0xFF) == ord("q"):
    #         break
    # # if we are not using a video file, stop the camera video stream
    # if not args.get("video", False):
    #     vs.stop()
    # # otherwise, release the camera
    # else:
    #     vs.release()
    # # close all windows
    # cv2.destroyAllWindows()

