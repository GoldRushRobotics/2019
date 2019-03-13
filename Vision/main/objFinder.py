import numpy as np
import cv2
import time

class foodFinder:

    def __init__(self,vs):

        self.vs = vs
        self.width = int(vs.get(3))
        self.height = int(vs.get(4))

        self.cube_cascade = cv2.CascadeClassifier('Cube11MarTraining/cascade.xml')
        self.ball_cascade = cv2.CascadeClassifier('Ball11MarTraining/cascade.xml')

        time.sleep(2)
        #self.tels_cascade = cv2.CascadeClassifier('telsCas16/cascade.xml')

    def findFood(self):

        ret, img = self.vs.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #cv2.imshow("fram",gray)
        # add this
        # image, reject levels level weights.
        balls = self.ball_cascade.detectMultiScale(gray, 2.25, 3)
        cubes = []
        #cubes = self.cube_cascade.detectMultiScale(gray, 3, 2)


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


        try:
            for x,y,w,h in objs:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 8)


        except:
            print("no obj found")

        show = cv2.resize(img,(480,270))
        cv2.imshow('frams',show)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            exit()
        try:
            return objs[0][0],objs[0][1]
        except:
            return -1,-1

