'''
This file contains the objFind class, which helps find objects. (food, tels, etc.)
'''

import numpy as np
import cv2
import time
import threading
from ColorFinder import findColor

# Create a my thread object class that can be used to multithread image
# analysis


class myThread(threading.Thread):

    def __init__(self, threadID, name, gray, finder, color=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.gray = gray
        self.color = color
        self.finder = finder
        self._return = None

    def run(self):
        print(self.threadID, self.name)
        if self.threadID == 1:
            self._return = self.finder.findFood(self.gray)
        elif self.threadID == 2:
            self._return = self.finder.findTels(self.gray)
        else:
            self._return = self.finder.findPill(self.gray, self.color)

    def getVals(self):
        return self._return


class objFind:

    '''
    objFind class takes a cv2 video stream and will return the largest objects in a given frame
    '''

    def __init__(self, vs, homeColor):

        self.vs = vs

        self.cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
        self.tels_cascade = cv2.CascadeClassifier('tels/cascade.xml')
        self.homeColor = homeColor

    def findObjs(self, food=True):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()

        img = cv2.flip(img, 0)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        avoidThread = myThread(2, "SpaceTelsThread", gray, self)
        avoidThread.start()

        if food:
            gotToThread = myThread(1, "FoodThread", gray, self)
        else:
            gotToThread = myThread(3, "PillThread", gray, self, color=img)

        gotToThread.start()

        # wait until both threads complete to return vals
        while 1:
            if gotToThread.isAlive() or avoidThread.isAlive():
                pass
            else:
                return (gotToThread.getVals(), avoidThread.getVals())

    def findFood(self, gray):

        balls = self.ball_cascade.detectMultiScale(
            gray, 2, minNeighbors=1, minSize=(25, 25))
        cubes = self.cube_cascade.detectMultiScale(
            gray, 2, minNeighbors=1, minSize=(25, 25))

        # Ensure that output is a list

        if len(balls) == 0:
            objs = cubes
        elif len(cubes) == 0:
            objs = balls
        else:
            # combine into a vStack
            objs = np.vstack((balls, cubes))

        # list(objs)
        # Sort in place wasnt working, dont @ me

        objs = sorted(objs, reverse=True, key=lambda x: x[3])
        # Biggest first

        try:
            return objs[0][0], objs[0][1]
        except:
            return -1, -1

    def findTels(self, gray):

        tels = self.tels_cascade.detectMultiScale(gray, 2, 5)

        tels = sorted(tels, reverse=True, key=lambda x: x[3])
        # Biggest first

        try:

            return tels[0][0], tels[0][1]
        except:
            return -1, -1

    def findPill(self, gray, colorImg):
        ##### TODO #####
        '''
        Nathan please put the pillar detector in here. Also, you can call the colorFinder code that is imported... Just pass in the location of the top left (x,y) as well as the width and height of the area and image.
        '''

        if findColor(colorImg, wRegion, hRegion, xRegion, yRegion) == self.homeColor:
            print("This pillar is our home color!")
        else:
            print("BLEH")

        return -1, -1
