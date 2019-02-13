import numpy as np
import cv2
import time

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#this is the cascade we just made. Call what you want
cube_cascade = cv2.CascadeClassifier('cubeCas16/cascade.xml')
ball_cascade = cv2.CascadeClassifier('ballCas16/cascade.xml')

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 240)

# prev = 0
# frame_rate = 240

while 1:
    # time_elapsed = time.time() - prev

    ret, img = cap.read()

    # if time_elapsed > 1./frame_rate:
    #     prev = time.time()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.resize(gray, (160*3, 90*3))


    # add this
    # image, reject levels level weights.
    balls = ball_cascade.detectMultiScale(gray, 2, 5)
    cubes = cube_cascade.detectMultiScale(gray, 3.5, 5)

    # add this
    for (x,y,w,h) in cubes:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        print("Cube at x={0}, y={1}".format(x,y))

    for (x,y,w,h) in balls:
        center = (x + w//2, y + h//2)
        cv2.circle(img, center, int(h/2), (0,255,255),2)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        print("Ball at x={0}, y={1}".format(x,y))

    #     # roi_gray = gray[y:y+h, x:x+w]
    #     # roi_color = img[y:y+h, x:x+w]
    #         # eyes = eye_cascade.detectMultiScale(roi_gray)
    #         # for (ex,ey,ew,eh) in eyes:
    #         #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
