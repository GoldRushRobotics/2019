import cv2
import numpy as np
import time

vs = cv2.VideoCapture(1)
# width = 600
# height = 600

time.sleep(2)

w = int(vs.get(3))
h = int(vs.get(4))

print("{0} {1}".format(w, h))


cube_cascade = cv2.CascadeClassifier('/home/matt19/Documents/Github/2019/Vision/main/cube/cascade.xml')
ball_cascade = cv2.CascadeClassifier('/home/matt19/Documents/Github/2019/Vision/main/ball/cascade.xml')

while True:
    ret, img = vs.read()

    # img = cv2.GaussianBlur(img, (3, 3), 2)
    # img = cv2.flip(img, 0)
    img = cv2.resize(img, (480, 270))
    # cv2.imshow('1', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # add this
    # image, reject levels level weights.
    balls = ball_cascade.detectMultiScale(
        gray, 2.5, minNeighbors=5, minSize=(64, 64), maxSize=(128, 128))
    cubes = cube_cascade.detectMultiScale(
        gray, 3.5, minNeighbors=5, minSize=(64, 64), maxSize=(128, 128))

    # Ensure that output is a list
    if len(balls) == 0 and len(cubes) == 0:
        objs = [(1, 1, 1, 1)]
        print("None")
    elif len(balls) == 0:
        objs = cubes
        print("Cubes")
        # cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
    elif len(cubes) == 0:
        objs = balls
        print("Balls")
        # cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
    else:
        # combine into a vStack
        objs = np.vstack((balls, cubes))
        print("Boths")

        # list(objs)
        # Sort in place wasnt working, dont @ me

    objs = sorted(objs, reverse=True, key=lambda x: x[3])

    (x, y, w, h) = objs[0]

    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # print(len(objs))
    # for (x, y, w, h) in objs:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    cv2.imshow('0', img)
    k = cv2.waitKey(100) & 0xFF  # large wait time to remove freezing
    if k == 113 or k == 27:
        break

cv2.destroyAllWindows()
