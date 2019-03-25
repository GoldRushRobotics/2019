'''
This file contains the objFind class, which helps find objects. (food, tels, etc.)
'''

import numpy as np
import cv2
import time
import threading


class myThread(threading.Thread):

    def __init__(self, threadID, name, gray, finder):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.gray = gray
        self.finder = finder
        self._return = None

    def run(self):
        print(self.threadID, self.name)
        if self.threadID % 2 == 0:
            self._return = self.finder.findFood(self.gray)
        else:
            self._return = self.finder.findTels(self.gray)

    def join(self):
        return self._return


class objFind:

    '''
    objFind class takes a cv2 video stream and will return the largest objects in a given frame
    '''

    def __init__(self, vs):

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

        # cv2.imshow('gray',gray)
        # k = cv2.waitKey(100) & 0xFF # large wait time to remove freezing
        # if k == 113 or k == 27:
        #     raise ValueError('BREAK OUT')
        thread1 = myThread(1, "Thread-1", gray, self)
        thread2 = myThread(2, "Thread-2", gray, self)

        thread1.start()
        thread2.start()

        while 1:
            if thread1.isAlive() or thread2.isAlive():
                pass
            else:
                return (thread1.join(), thread2.join())

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
