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

    pt1 = (x, y)
    pt2 = (x + width, y + height)

    color = ' '

    # img[height_range, width_range]
    cropped = image[pt1[1]:pt2[1], pt1[0]:pt2[0]]

    totalPix = (0, 0, 0)

    for h in range(0, width - 1):
        for w in range(0, height - 1):
            print(cropped[w][h])
            totalPix = totalPix + cropped[w][h]

    avgPix = totalPix / ((width) * (height))
    print(avgPix)

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
    cv2.imwrite("cropped.jpg", cropped)

    return color
