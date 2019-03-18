import numpy as np
import cv2
import time


class telsFinder:

    def __init__(self,vs,w,h):

        self.vs = vs
        self.width = w
        self.height = h

        self.tels_cascade = cv2.CascadeClassifier('tels/cascade.xml')

    def findTel(self):

        ret, img = self.vs.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        tels = self.tels_cascade.detectMultiScale(gray, 2, 5)

        # Ensure that output is a list
        # list(tels)
        # Sort em
        #print(type(tels))

        tels = sorted(tels, reverse=True, key=lambda x: x[3])
        # Biggest first
        # tels.reverse()

        try:

            return tels[0][0],tels[0][1]
        except:
            return -1,-1

class foodFinder:

    def __init__(self,vs,w,h):

        self.vs = vs
        self.width = w
        self.height = h

        self.cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')

    def findFood(self):

        ret, img = self.vs.read()

        # img = cv2.resize(img, (int(self.width/2), int(self.height/2))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("fram",gray)
        # add this
        # image, reject levels level weights.
        balls = self.ball_cascade.detectMultiScale(gray, 2, 2)
        cubes = self.cube_cascade.detectMultiScale(gray, 2, 2)

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


        # print(type(objs))
        # objs.sort(reverse=True, key=lambda x: x[3])
        # objs.reverse()
        img = cv2.resize(img, (int(self.width/4), int(self.height/4)))
        for x,y,w,h in objs:
            x,y,w,h = x/4,y/4,w/4,h/4
            cv2.rectangle(img,(x, y), (x+w, y+h),(255,255,0),2)

        cv2.imshow('img',img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            exit()



        try:

            return objs[0][0],objs[0][1]
        except:
            return -1,-1
