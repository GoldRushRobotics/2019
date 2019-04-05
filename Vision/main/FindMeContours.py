'''

This is currently some adapted code from our refrence library. The loop() function should probably be moved out into main.


'''


# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time
import numpy
#import cython
import math
#from cython import threshold_fast



def setup():
    # construct the argument parse and parse the arguments


    # if a video path was not supplied, grab the reference
    # to the webcam
    vs = cv2.VideoCapture(0)
    time.sleep(1)
    return vs, True


def death(vs, args):
    # if we are not using a video file, stop the camera video stream
    vs.release()

    # close all windows
    cv2.destroyAllWindows()

# def is_contour_bad(c):
#   # approximate the contour
#   peri = cv2.arcLength(c, True)
#   approx = cv2.approxPolyDP(c, 0.02 * peri, True)

#   # the contour is 'bad' if it is not a rectangle
#   return not len(approx) == 4

def isWhite(rgb):
    return True

def loop(vs, ret):
    sections = 4
    kernel_height = math.floor(450/sections)
    kernel_width = 6
    kernel = [numpy.array([-1,-1,-1,1,1,1])]  * kernel_height
    shifted = [[x for x in range(0,100)]] * sections
    while True:
        # grab the current frame
        ret, frame = vs.read()

        # TODO: If above edited fix

        # handle the frame from VideoCapture or VideoStream

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if not ret:
            break

        # resize the frame, blur it, and convert it to the gray
        # color space

        # TODO: maybe not resize or blur?
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (15, 15), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        mask = cv2.Canny(gray, 25, 40)
        for y in range(0, mask.shape[0]):
            for x in range(0, mask.shape[1]):
                if mask[y][x] == 255:
                    if not isWhite(frame[y][x-3]):
                        mask[y][x] = 0 #there is a pillar or center here
#kernel thought of better idea using white as reference
#        for y in range(4):
#            for x in range(math.floor(mask.shape[1]/kernel_width)):
#                #crop = mask[x*kernel_width:(x+1)*kernel_width][y*kernel_height:(y+1)*kernel_height]
#                #crop = mask[0:112][0:6] # gives 6x600 for some reason
#                crop  = [[100,100,100,0,0,0]]  * kernel_height
#                #print(numpy.shape(kernel))
#                #print(numpy.shape(crop))
#                #print(crop * kernel)
#                val = 0;
#                for j in range(kernel_height-1):
#                    for k in range(kernel_width-1):
#                        val = val + crop[j][k] * kernel[j][k]
#                val = val / (kernel_width * kernel_height)
#                if abs(val) >= 50:
#                    shifted[y][x] = 255
#                else:
#                    shifted[y][x] = 0
#        #cv2.imshow("shifted", shifted)
#        print(shifted)

# slow and clunky
#        for y in range(0, mask.shape[0]-2):
#            for x in range(0, mask.shape[1]):
#                if(mask[y][x] == 255):
#                    if(mask[y+1][x] != 255):
#                        mask[y][x] = 0
#                        if(mask[y+2][x] != 255):
#                            mask[y+1][x] = 0
#        mask = threshold_fast(mask)

        
        # TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
        # find contours in the mask and initialize the current
        # (x, y) center of the ball

        # RETR_EXTERNAL is another option to RETR_TREE
#        cnts = cv2.findContours(
#            mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        #cnts = imutils.grab_contours(cnts)
#        ctrs = numpy.array(cnts).reshape((-1, 1, 2)).astype(numpy.int32)
#        maskinverse = numpy.ones(frame.shape[:2], dtype="uint8") * 255

        # remove the contours from the image and show the resulting images
#        mask = cv2.bitwise_and(mask, mask, mask=maskinverse)


#    ctrs = numpy.array(cnts).reshape((-1,1,2)).astype(numpy.int32)
#    img = cv2.drawContours(mask, ctrs, -1, (0,255,0), 3)



        # TODO: Make dict for contour arrays and loop
        # only proceed if at least one contour was found
#        if len(ctrs) > 0:
#            # find the largest contour in the mask, then use
#            # it to compute the minimum enclosing circle and
#            # centroid'
#            for ctr in ctrs:
#                break

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Gray", gray)
        # if the 'q' key is pressed, stop the loop
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break



if __name__ == '__main__':
    vs, ret = setup()
    loop(vs, ret)
    death(vs, ret)