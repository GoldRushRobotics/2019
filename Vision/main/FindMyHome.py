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

    actColor = ' '
    H_Upper = 225
    H_Lower = 350
    W_Upper = 400
    W_Lower = 250

    hDiff = H_Lower - H_Upper
    wDiff = W_Upper - W_Lower

    cropped = image[W_Lower:W_Upper,H_Upper:H_Lower] #img[height_range, width_range]

    #       lower bound , upper bound
    b = ([102, 0, 0], [255, 204, 204])
    g = ([0, 0, 0], [75, 255, 75])
    y = ([0, 160, 170], [220, 255, 255])
    r = ([0, 0, 118], [194, 194, 255])


    totalPix = (0, 0, 0)

    for h in range(0, hDiff - 1):
        for w in range(0, wDiff - 1):
            totalPix = totalPix + cropped[w][h]

    avgPix = totalPix / ((wDiff) * (hDiff))

    # pix = [avgPix[0], avgPix[1], avgPix[2]]

    col = []
    colors = ['r', 'g', 'b', 'y']


    for color in (r, g, b, y):
        low, up = color
        isCol = True
        for i, x in enumerate(avgPix):
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
