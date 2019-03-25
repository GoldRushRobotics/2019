import cv2
import numpy as np
import time

vs = cv2.VideoCapture(0)
#width = 600
#height = 600

time.sleep(2)


cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
while True:
    ret, img = vs.read()
    img = cv2.flip(img, 0)
    img = cv2.resize(img, (int(vs.get(3) / 2), int(vs.get(4) / 2)))
    # cv2.imshow('1', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # add this
    # image, reject levels level weights.
    balls = ball_cascade.detectMultiScale(
        gray, 2, minNeighbors=3, minSize=(25, 25))
    cubes = cube_cascade.detectMultiScale(
        gray, 2, minNeighbors=3, minSize=(25, 25))

    # Ensure that output is a list
    if len(balls) == 0 and len(cubes) == 0:
        objs = [[1, 1, 1, 1]]
        # print("")
    elif len(balls) == 0:
        objs = cubes
        # cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
    elif len(cubes) == 0:
        objs = balls
        # cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
    else:
                # combine into a vStack
        objs = np.vstack((balls, cubes))

        # list(objs)
        # Sort in place wasnt working, dont @ me

    objs = sorted(objs, reverse=True, key=lambda x: x[3])
    print(len(objs))
    for (x, y, w, h) in objs:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    cv2.imshow('0', img)
    k = cv2.waitKey(100) & 0xFF  # large wait time to remove freezing
    if k == 113 or k == 27:
        break

cv2.destroyAllWindows()
