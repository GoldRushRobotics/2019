import urllib.request
import cv2
import numpy as np
import os
import time
import re
import sys
# from imutils.video import VideoCapture
#vs = cv2.VideoCapture('training/IMG_0024.MOV')

outPath = sys.argv[2]
inPath = sys.argv[1]
#time.sleep(2)


if not os.path.exists(outPath):
  os.makedirs(outPath)

def captureVideo(vs,outPath):


  num = 200000


  while(True):
    # Capture frame-by-frame
    ret, current_frame = vs.read()
    if type(current_frame) == type(None):
        print("noFrame")
        break


    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (128, 128))
    cv2.imshow('preview',gray)
    cv2.imwrite(outPath+str(num)+'.jpg',gray)
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
def bitand(inpath):
    files = os.listdir(inPath)

    mask = cv2.imread(inPath+files[0],0)

    for file in files:
        gray = cv2.imread(inPath+file,0)
        mask = cv2.bitwise_and(gray, mask)

    cv2.imshow("blah",mask)


def fromImgs(inPath,outPath):


  num = 20


  files = os.listdir(inPath)

  for file in files:
    print(inPath+file)
    # Capture frame-by-frame
    gray = cv2.imread(inPath+file,0)
    # ret, current_frame = vs.read()
    # if type(current_frame) == type(None):
    #     print("noFrame")
    #     break


    # gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (64, 64))
    #cv2.imshow('preview',gray)
    cv2.imwrite(outPath+str(num)+'.png',gray)
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


bitand(outPath)
#fromImgs(inPath,outPath)
#captureVideo(vs,outPath)
