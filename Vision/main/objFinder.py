import numpy as np
import cv2
import time

class foodFinder:

    def __init__(self,vs):

        self.vs = vs
        self.width = int(vs.get(3))
        self.height = int(vs.get(4))

        self.cube_cascade = cv2.CascadeClassifier('cubeCas16/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('ballCas16/cascade.xml')

        time.sleep(2)
        #self.tels_cascade = cv2.CascadeClassifier('telsCas16/cascade.xml')

    def findFood(self):

        ret, img = self.vs.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("fram",gray)
        # add this
        # image, reject levels level weights.
        balls = self.ball_cascade.detectMultiScale(gray, 2.5, 5)
        cubes = self.cube_cascade.detectMultiScale(gray, 2.5, 5)


        if len(balls) == 0:
            objs = cubes
        elif len(cubes) == 0:
            objs = balls
        else:
            # combine into a vStack
            objs = np.vstack((balls, cubes))

        # Sort in place wasnt working, dont @ me
        # objs.sort(key=lambda, x: x[3])

        objs = sorted(objs, key=lambda x: x[3])
        # Biggest first

        objs.reverse()
        print(objs)
        try:
            return objs[0][0],objs[0][1]
        except:
            return -1,-1

