'''
This file contains the objFind class, which helps find objects. (food, tels, etc.)
'''

import numpy as np
import cv2
import time
from MultiThreading import threadedFind
from ColorFinder import findColor


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

        self.colorImg = None
        self.grayImg = None

    def findObjs(self, food=True, goHome=False):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()

        self.img = cv2.flip(img, 0)

        self.grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        avoidThread = threadedFind(2, "TelsThread", self)
        avoidThread.start()

        if food:
            gotToThread = threadedFind(1, "FoodThread", self)
        else:
            gotToThread = threadedFind(
                3, "PillThread", self, goHome=goHome)

        gotToThread.start()

        # wait until both threads complete to return vals
        while 1:
            if gotToThread.isAlive() or avoidThread.isAlive():
                pass
            else:
                return (gotToThread.getVals(), avoidThread.getVals())

    def findFood(self):

        balls = self.ball_cascade.detectMultiScale(
            self.grayImg, 2, minNeighbors=1, minSize=(25, 25))
        cubes = self.cube_cascade.detectMultiScale(
            self.grayImg, 2, minNeighbors=1, minSize=(25, 25))

        # Ensure that output is a list

        if len(balls) == 0:
            objs = cubes
        elif len(cubes) == 0:
            objs = balls
        else:
            # combine into a vStack
            objs = np.vstack((balls, cubes))

        # Sort from largest to smallest
        objs = sorted(objs, reverse=True, key=lambda x: x[3])

        try:
            return objs[0][0], objs[0][1]
        except:
            return -1, -1

    def findTels(self):

        tels = self.tels_cascade.detectMultiScale(self.grayImg, 2, 5)

        # Sort from largest to smallest
        tels = sorted(tels, reverse=True, key=lambda x: x[3])

        try:

            return tels[0][0], tels[0][1]
        except:
            return -1, -1

    def findPill(self, goHome):

        # v This stuff exists v
        #   gray = self.grayImg
        # colorImg = self.colorImg
        # homeColor = self.homeColor

        ##### TODO #####
        '''
        Nathan please put the pillar detector in here. Also, you can call the colorFinder code that is imported... Just pass in the location of the top left (x,y) as well as the width and height of the area and image.
        '''

        if findColor(colorImg, wRegion, hRegion, xRegion, yRegion) == self.homeColor:
            print("This pillar is our home color!")
        else:
            print("BLEH")

        return -1, -1
