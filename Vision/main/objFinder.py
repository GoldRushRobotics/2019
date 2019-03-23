'''
This file contains the objFind class, which helps find objects. (food, tels, etc.)
'''

import numpy as np
import cv2
import time

class objFind:

    '''
    objFind class takes a cv2 video stream and will return the largest objects in a given frame
    '''

    def __init__(self,vs):

        self.vs = vs

        self.cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
        self.tels_cascade = cv2.CascadeClassifier('tels/cascade.xml')


    def findObjs(self):
        '''
        Returns tuple of the two largest objects (food, tels) according to the current grayscale image.
        '''
        ret, img = self.vs.read()

        img = cv2.flip(img, 0)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('gray',gray)
        k = cv2.waitKey(100) & 0xFF # large wait time to remove freezing
        if k == 113 or k == 27:
            raise ValueError('BREAK OUT')

        return (self.findFood(gray), self.findTels(gray))


    def findFood(self, gray):

        balls = self.ball_cascade.detectMultiScale(gray, 2, minNeighbors = 1, minSize = (25,25))
        cubes = self.cube_cascade.detectMultiScale(gray, 2, minNeighbors = 1, minSize =  (25,25))


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
            return objs[0][0],objs[0][1]
        except:
            return -1,-1

    def findTels(self, gray):

        tels = self.tels_cascade.detectMultiScale(gray, 2, 5)

        tels = sorted(tels, reverse=True, key=lambda x: x[3])
        # Biggest first

        try:

            return tels[0][0],tels[0][1]
        except:
            return -1,-1

