'''
Finds the color of a specified image when passed a color image
'''

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time


def findColor(image, width, height, x, y):
    '''
    Finds the color of a given image region.
    This function takes an image, the width and height of the region, as well as the x,y location of the top left of the region.
    '''

    color = ' '
    H_Upper = y - height
    H_Lower = y
    W_Upper = x + width
    W_Lower = x

    # Old values

    # H_Upper = 225
    # H_Lower = 350
    # W_Upper = 400
    # W_Lower = 250

    hDiff = H_Lower - H_Upper
    wDiff = W_Upper - W_Lower

    # img[height_range, width_range]
    cropped = image[W_Lower:W_Upper, H_Upper:H_Lower]

    # cv2.imshow('img',cropped)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        exit()

    totalPix = (0, 0, 0)

    for h in range(0, hDiff - 1):
        for w in range(0, wDiff - 1):
            totalPix = totalPix + cropped[w][h]

    avgPix = totalPix / ((wDiff) * (hDiff))

    # print(avgPix)

    colors = {"b": (255, 0, 0),
              "g": (0, 255, 0),
              "r": (0, 0, 255),
              "y": (0, 180, 255)
              }

    manhattan = lambda x, y: abs(x[0] - y[0]) + \
        abs(x[1] - y[1]) + abs(x[2] - y[2])
    distances = {k: manhattan(v, avgPix) for k, v in colors.items()}
    color = min(distances, key=distances.get)

   # print(color)

    return color
