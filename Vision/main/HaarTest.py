import cv2
vs = cv2.VideoCapture(1)
width = 600
height = 600

cube_cascade = cv2.CascadeClassifier('cube/cascade.xml')
ball_cascade = cv2.CascadeClassifier('ball/cascade.xml')
while(True):
    ret, img = vs.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # add this
            # image, reject levels level weights.
    balls = ball_cascade.detectMultiScale(gray, 2, 2)
    cubes = cube_cascade.detectMultiScale(gray, 2, 2)

            # Ensure that output is a list
    if len(balls) == 0 and len(cubes)==0:
        cv2.imshow('0', img)
    elif len(balls) == 0:
        objs = cubes
        cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
        cv2.imshow('1',img)
    elif len(cubes) == 0:
        objs = balls
        cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
        cv2.imshow('2',img)
    else:
                # combine into a vStack
        objs = np.vstack((balls, cubes))

            # list(objs)
            # Sort in place wasnt working, dont @ me

        objs = sorted(objs, reverse=True, key=lambda x: x[3])
        cv2.circle(img, (objs[0][0], objs[0][1]), 50, (255, 255, 255), 2)
        cv2.imshow('3',img)