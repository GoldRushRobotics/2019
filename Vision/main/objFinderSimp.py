'''
This file contains the objFind class, which helps find objects. (food, tels, etc.)
'''

import numpy as np
import cv2
import time
from MultiThreading import threadedFind
from ColorFinder import findColor
from Poop import objPoop


class objFind:

    '''
    objFind class takes a cv2 video stream and will return the largest objects in a given frame
    '''

    def __init__(self, vs, homeColor, movmt):

        self.vs = vs
        self.movmt = movmt

        self.cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
        self.tels_cascade = cv2.CascadeClassifier('tels/cascade.xml')
        self.homeColor = homeColor
        self.recentPil = 0

        self.colorImg = None
        self.grayImg = None
        self.colorDict = {"b": ("r", "g", "y"), "r": (
            "b", "g", "y"), "y": ("g", "b", "r"), "g": ("y", "b", "r")}

    def findObjs(self, food=True, goHome=False):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()
        # img = cv2.resize(img, (64, 36))
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
            self.grayImg, 3.5, minNeighbors=5, maxSize=(128, 128))
        cubes = self.cube_cascade.detectMultiScale(
            self.grayImg, 3, minNeighbors=5, maxSize=(128, 128))

        # Ensure that output is a list
        if len(balls) == 0 and len(cubes) == 0:
            return -1, -1 , None
        elif len(balls) == 0:
            objs = cubes
        elif len(cubes) == 0:
            objs = balls
        else:
            # combine into a vStack
            objs = np.vstack((balls, cubes))

        # Sort from largest to smallest
        objs = sorted(objs, reverse=True, key=lambda x: x[3])

        return objs[0][0], objs[0][1], None

    def findTels(self):

        tels = self.tels_cascade.detectMultiScale(
            self.grayImg, 3.5, minNeighbors=4, maxSize=(128, 128))

        # Sort from largest to smallest
        tels = sorted(tels, reverse=True, key=lambda x: x[3])

        try:

            return tels[0][0], tels[0][1], None
        except:
            return -1, -1, None

    def findPill(self, goHome):
        WIDTH_CHECK = 2
        LEAST_HEIGHT = 5
        NUMBER_OF_FRAMES = 20
        # v This stuff exists v
        #   gray = self.grayImg
        # colorImg = self.colorImg
        # homeColor = self.homeColor
        gray = cv2.GaussianBlur(self.grayImg, (5, 5), 0)
        mask = cv2.Canny(gray, 25, 40)
        for y in range(0, mask.shape[0]):
            for x in range(0, mask.shape[1] - WIDTH_CHECK):
                if mask[y][x] == 255:
                    if not isWhite(frame[y][x - WIDTH_CHECK]):
                        mask[y][x] = 0
                    elif not isWhite(frame[y][x + WIDTH_CHECK]):
                        mask[y][x] = 0
                    else:
                        count = 0
                        while(mask[y - count][x] == 255):
                            count = count + 1
                            if y - count < 0:
                                break
                        if(count > LEAST_HEIGHT):
                            color = findColor(
                                self.colorImg, WIDTH_CHECK * 2 + 1, count, x, y)
                            if(self.recentPil == 2):
                                countF = 0
                                objPoop(count, WIDTH_CHECK *
                                        2 + 1, color, x, y)
                            elif(goHome):
                                if(self.colorDict[self.homeColor](0) == color):
                                    return x, y, color
                                else:
                                    return -1, -1, color
                            elif(self.colorDict[self.homeColor](1) == color or self.colorDict[self.homeColor](2) == color):
                                return x, y, color
                            else:
                                return -1, -1, color
                            self.recentPil = 1
                        elif(self.recentPil == 1):
                            
                            countF = countF + 1
                            if(countF == NUMBER_OF_FRAMES):
                                #self.recentPil = 2
                                self.movmt.writeArray("w64")


# function prototype        findColor(colorImg, wRegion, hRegion, xRegion,
# yRegion)
        return -1, -1, None  # final return error catch
