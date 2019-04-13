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

        self.blue = ((95, 109, 0), (117, 255, 255))

        self.green = ((35, 115, 0), (86, 255, 255))

        self.yellow = ((13, 71, 0), (26, 255, 255))

        self.red = ((0, 118, 0), (6, 255, 255))

        self.st = ((10, 60, 0), (17, 255, 255))

        # self.cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
        # self.ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
        # self.tels_cascade = cv2.CascadeClassifier('tels/cascade.xml')
        self.homeColor = homeColor
        self.recentPil = 0

        self.colorImg = None
        self.grayImg = None
        self.hsvImg = None
        # Fucking dict of tuples of strings. Nasty.
        self.colorDict = {"b": ("r", "g", "y"), "r": (
            "b", "g", "y"), "y": ("g", "b", "r"), "g": ("y", "b", "r")}

    def findObjs(self, food=True, goHome=False):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()
        # img = cv2.resize(img, (64, 36))
        # self.img = cv2.flip(img, 0)
        self.hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        self.grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if goHome:
            thread0 = threadedFind(
                3, "PillThread", self, goHome=goHome)
        else:
            for num, i in enumerate(["r", "g", "b", "y", "st"]):
                thread = threadedFind(num, "{0}Thread".format(i), self, i)
                thread.start()
                exec("thread{0}=thread".format(num))

        # wait until both threads complete to return vals
        while 1:
            if thread0.isAlive() or thread1.isAlive() or thread2.isAlive() or thread3.isAlive() or thread4.isAlive():
                pass
            else:
                food = []
                tels = []
                pill = []
                for thread in thread0, thread1, thread2, thread3, thread4:
                    f, t, p = thread0.getVals()
                    food.append(f)
                    tels.append(t)
                    pill.append(p)

                food = sorted(food, reverse=True, key=lambda x: x[3])
                tels = sorted(tels, reverse=True, key=lambda x: x[3])
                pill = sorted(pill, reverse=True, key=lambda x: x[3])

                return (foods, tels)

    def findColored(self, color):
        tels = [(0,0,0,0)]
        food = [(0,0,0,0)]
        pill = [(0,0,0,0)]

        if color == "r":
            mask = cv2.inRange(self.hsv, self.red)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

        elif color == "g":
            mask = cv2.inRange(self.hsv, self.green)
            mask = cv2.erode(mask, None, iterations=1)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=1)

        elif color == "b":
            mask = cv2.inRange(self.hsv, self.blue)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=1)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=3)

        elif color == "y":
            mask = cv2.inRange(self.hsv, self.yellow)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

        elif color == "st":
            mask = cv2.inRange(self.hsv, self.st)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

        else:
            return food, tels, pill

        dictionary = {}
        dictionary['cnts'] = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        dictionary['cnts'] = dictionary['cnts'][
            0] if imutils.is_cv2() else dictionary['cnts'][1]

        for key, cnts in dictionary.items():
            if not (dictionary[key]) == None:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                for cB in dictionary[key]:
                    approx = cv2.approxPolyDP(
                        cB, 0.01 * cv2.arcLength(cB, True), True)
                    if len(approx) <= NUM_SIDES:
                        x, y, w, h = cv2.boundingRect(cB)
                        if not (h > w * 2) and color == "st":
                            tels.append((x, y, w, h))
                        elif not (h > w * 2):
                            food.append((x, y, w, h))
                        else:
                            pill.append((x, y, w, h))

                    elif len(approx) > NUM_SIDES:
                        ((x, y), radius) = cv2.minEnclosingCircle(cB)
                        mB = cv2.moments(cB)
                        # centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))
                        # only proceed if the radius meets a minimum size
                        if radiusB * 1.5 > MIN_VALUE and color == "st":
                            tels.append((x, y, 2 * radius, 2 * radius))
                        elif radiusB * 1.5 > MIN_VALUE:
                            food.append((x, y, 2 * radius, 2 * radius))

        food = sorted(food, reverse=True, key=lambda x: x[3])
        tels = sorted(tels, reverse=True, key=lambda x: x[3])
        pill = sorted(pill, reverse=True, key=lambda x: x[3])

        return food[0], tels[0], pill[0]

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
                            self.movmt.writeArray("s64")
                            countF = countF + 1
                            if(countF > NUMBER_OF_FRAMES):
                                self.recentPil = 2


# function prototype        findColor(colorImg, wRegion, hRegion, xRegion,
# yRegion)
        return -1, -1, None  # final return error catch
