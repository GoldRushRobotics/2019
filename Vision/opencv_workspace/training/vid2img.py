import urllib.request
import cv2
import numpy as np
import os
import time
import re
import sys
import threading
import psutil
# from imutils.video import VideoCapture


outPath = sys.argv[2]
inPath = sys.argv[1]
# time.sleep(2)


class myThread(threading.Thread):

    def __init__(self, threadID, current_frame, outPath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.current_frame = current_frame
        self.outPath = outPath

    def run(self):
        print('{0}.jpg'.format(self.threadID))
        self.gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.resize(self.gray, (240, 135))
        #cv2.imshow('preview', gray)
        cv2.imwrite(self.outPath + str(self.threadID) + '.jpg', self.gray)


if not os.path.exists(outPath):
    os.makedirs(outPath)


def captureVideo(inPath, outPath):

    vs = cv2.VideoCapture(inPath)

    process = psutil.Process(os.getpid())

    num = 58352

    while(True):
        # Capture frame-by-frame
        # if process.memory_info().rss >= 40000000000:
        #     time.sleep(1)
        #     print(process.memory_info().rss)
        #     continue

        ret, current_frame = vs.read()
        if type(current_frame) == type(None):
            print("noFrame")
            break

        print('{0}.jpg'.format(num))
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (240, 135))
        #cv2.imshow('preview', gray)
        cv2.imwrite(outPath + str(num) + '.jpg', gray)

        # thread = myThread(num, current_frame, outPath)

        # thread.start()

        # exec('thread{0} = thread'.format(num))

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

    mask = cv2.imread(inPath + files[0], 0)

    for file in files:
        gray = cv2.imread(inPath + file, 0)
        mask = cv2.bitwise_and(gray, mask)

    cv2.imshow("blah", mask)


def fromImgs(inPath, outPath):

    num = 58352

    files = os.listdir(inPath)

    for file in files:
        print(inPath + file)
        # Capture frame-by-frame
        gray = cv2.imread(inPath + file, 0)
        # ret, current_frame = vs.read()
        # if type(current_frame) == type(None):
        #     print("noFrame")
        #     break

        # gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (64, 64))
        # cv2.imshow('preview',gray)
        cv2.imwrite(outPath + str(num) + '.png', gray)
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


# bitand(outPath)
# fromImgs(inPath,outPath)
captureVideo(inPath, outPath)
