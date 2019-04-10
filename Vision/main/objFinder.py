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
        self.colorDict = {"b":("r","g", "y"), "r":("b","g", "y"), "y":("g","b","r"), "g":("y","b","r")}

    def findObjs(self, food=True, goHome=False):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()
        img = cv2.resize(img, (64,36))
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
        WIDTH_CHECK = 2
        # v This stuff exists v
        #   gray = self.grayImg
        # colorImg = self.colorImg
        # homeColor = self.homeColor
        gray = cv2.GaussianBlur(self.grayImg, (15, 15), 0)
        mask = cv2.Canny(gray, 25, 40)
        for y in range(0, mask.shape[0]):
            for x in range(0, mask.shape[1]-WIDTH_CHECK):
                if mask[y][x] == 255:
                    if not isWhite(frame[y][x - WIDTH_CHECK]):
                    else if not isWhite(frame[y][x + WIDTH_CHECK]):
                        mask[y][x] = 0
                    else:
                        count = 0
                        while(mask[y-count][x] == 255):
                            count = count + 1
                            if y-count < 0:
                                break
                        color = findColor(self.colorImg, WIDTH_CHECK*2+1, count, x, y)
                        if(goHome):
                            if(self.colorDict[self.homeColor](0) == color):
                                return x, y, color
                            else:
                                return -1, -1
                        else if(self.colorDict[self.homeColor](1) == color or self.colorDict[self.homeColor](2) == color):
                            return x, y, color
                        else:
                            return -1, -1



        ##### TODO #####
        '''
        Nathan please put the pillar detector in here. Also, you can call the colorFinder code that is imported... Just pass in the location of the top left (x,y) as well as the width and height of the area and image.
        '''

        if findColor(colorImg, wRegion, hRegion, xRegion, yRegion) == self.homeColor:
            print("This pillar is our home color!")
        else:
            print("BLEH")

        return -1, -1
