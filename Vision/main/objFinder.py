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
        balls = self.ball_cascade.detectMultiScale(gray, 2, 5)
        cubes = self.cube_cascade.detectMultiScale(gray, 2, 5)


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






        # add this
        # for (x,y,w,h) in cubes:
        #     center = (x + w//2, y + h//2)
        #     cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        #     print("Cube at x={0}, y={1}".format(x,y))

        # for (x,y,w,h) in balls:
        #     center = (x + w//2, y + h//2)
        #     cv2.circle(img, center, int(h/2), (0,255,255),2)
        #     #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #     print("Ball at x={0}, y={1}".format(x,y))


        #cv2.imshow('img',img)
