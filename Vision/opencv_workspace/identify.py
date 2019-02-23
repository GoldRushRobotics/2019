import numpy as np
import cv2
import time
import imutils
from movement import mov

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#this is the cascade we just made. Call what you want
cube_cascade = cv2.CascadeClassifier('cubeCas16/cascade.xml')
ball_cascade = cv2.CascadeClassifier('ballCas16/cascade.xml')

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 240)


#gray = cv2.resize(gray, (128,128))


# add this
# image, reject levels level weights.

mover = mov(int(cap.get(3)),int(cap.get(4)))

try:
    while 1:
        ret, img = cap.read()
       	img = imutils.rotate(img, 180)
	# cv.Flip(img,flipMode=-1)

        # if time_elapsed > 1./frame_rate:
        #     prev = time.time()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        balls = ball_cascade.detectMultiScale(gray, scaleFactor=3, minNeighbors=1, minSize=(55,55))
        cubes = cube_cascade.detectMultiScale(gray, 2, 5)
        # add this
        for (x,y,w,h) in cubes:
            cv2.rectangle(gray,(x,y),(x+w,y+h),(255,255,0),2)
        #     print("Cube at x={0}, y={1}".format(x,y))



        for (x,y,w,h) in balls:
            center = (x + w//2, y + h//2)
            cv2.circle(gray, center, int(h/2), (0,255,255),2)
            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #print("Ball at x={0}, y={1}".format(x,y))

        if len(balls) == 0:
            objs = cubes
        elif len(cubes) == 0:
            objs = balls
        else:
        #     # combine into a vStack
            objs = np.vstack((balls, cubes))

        objs = sorted(objs, key=lambda x: x[3])
        # Biggest first

        objs.reverse()
        if len(objs) > 0:
            mover.whereToGo(objs[0][0],objs[0][1])
        else:
            mover.whereToGo(-1,-1)
        mover.goToWhere()

        cv2.imshow('img', gray)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        #time.sleep(.5)
except KeyboardInterrupt:
    mover.writeArray('a0')
    mover.writeArray('w0')
    mover.ser.close()
    cv2.destroyAllWindows()

mover.writeArray('a0')
mover.writeArray('w0')
mover.ser.close()
cv2.destroyAllWindows()
