import urllib.request
import cv2
import numpy as np
import os
import time
# from imutils.video import VideoCapture
vs = cv2.VideoCapture(1)
path = 'courseNeg'
time.sleep(2)


if not os.path.exists(path):
  os.makedirs(path)

def captureVideo(vs):


  num = 1761


  while(True):
    # Capture frame-by-frame
    ret, current_frame = vs.read()
    if type(current_frame) == type(None):
        print("noFrame")
        break


    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (128, 128))
    cv2.imshow('preview',gray)
    cv2.imwrite(path+'/'+str(num)+'.jpg',gray)
    num += 1
    # Display the resulting frame

    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #     # cv2.imshow('captured',gray)
    #     cv2.imwrite(path+'/'+str(num)+'.jpg',gray)
    #     num += 1
    #     # time.sleep(.2)
    #     # cv2.destroyAllWindows()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



captureVideo(vs)
