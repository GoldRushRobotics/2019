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
<<<<<<< HEAD
import numpy


# TODO: Fix if needed due to no reference video being passed will always be webcam (speed on startup concerns)
def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4
=======


# TODO: Fix if needed due to no reference video being passed will always be webcam (speed on startup concerns)
>>>>>>> 5260c724b530e764e63d99257073e48c24688c8e

def setup():
  # construct the argument parse and parse the arguments
  ap = argparse.ArgumentParser()
  ap.add_argument("-v", "--video",
                  help="path to the (optional) video file")
  ap.add_argument("-b", "--buffer", type=int, default=64,
                  help="max buffer size")
  args = vars(ap.parse_args())

  # TODO: Removes Arguments from buffer Im pretty sure
  pts = deque(maxlen=args["buffer"])

  # if a video path was not supplied, grab the reference
  # to the webcam
  if not args.get("video", False):
      vs = VideoStream(src=1).start()

  # otherwise, grab a reference to the video file
  else:
      vs = cv2.VideoCapture(args["video"])

  return vs, args

def death(vs,args):
    # if we are not using a video file, stop the camera video stream
  if not args.get("video", False):
      vs.stop()

  # otherwise, release the camera
  else:
      vs.release()

  # close all windows
  cv2.destroyAllWindows()

# def is_contour_bad(c):
#   # approximate the contour
#   peri = cv2.arcLength(c, True)
#   approx = cv2.approxPolyDP(c, 0.02 * peri, True)

#   # the contour is 'bad' if it is not a rectangle
#   return not len(approx) == 4

def loop(vs,args):
<<<<<<< HEAD
  while True:
    # grab the current frame
    frame = vs.read()

    # TODO: If above edited fix

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the gray
    # color space

    # TODO: maybe not resize or blur?
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # mask = cv2.inRange(gray, blueLower, blueUpper)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.Canny(gray, 25, 40)

    # TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    
    #RETR_EXTERNAL is another option to RETR_TREE
    cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    #cnts = imutils.grab_contours(cnts)
    ctrs = numpy.array(cnts).reshape((-1,1,2)).astype(numpy.int32)
    maskinverse = numpy.ones(frame.shape[:2], dtype="uint8") * 255
 
    # loop over the contours
    for c in ctrs:
    	# if the contour is bad, draw it on the mask
    	if is_contour_bad(c):
    		cv2.drawContours(maskinverse, [c], -1, 0, -1)
 
    # remove the contours from the image and show the resulting images
    mask = cv2.bitwise_and(mask, mask, mask=maskinverse)


#    ctrs = numpy.array(cnts).reshape((-1,1,2)).astype(numpy.int32)
#    img = cv2.drawContours(mask, ctrs, -1, (0,255,0), 3)
    
    
    ################################################################################
#    #watershed
#    
#    # noise removal
#    kernel = numpy.ones((3,3),numpy.uint8)
#    opening = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel, iterations = 2)
#    # sure background area
#    sure_bg = cv2.dilate(opening,kernel,iterations=3)
#    
#    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
#    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#    # Finding unknown region
#    sure_fg = numpy.uint8(sure_fg)
#    unknown = cv2.subtract(sure_bg,sure_fg)
#    # Marker labelling
#    ret, markers = cv2.connectedComponents(sure_fg)
#    # Add one to all labels so that sure background is not 0, but 1
#    markers = markers+1
#    # Now, mark the region of unknown with zero
#    markers[unknown==255] = 0
#    markers = cv2.watershed(frame,markers)
#    frame[markers == -1] = [255,0,0]
    
    ##############################################################################
#    #Kmeans segmentation
#    #not working
#    
#
#    # convert to np.float32
#    Z = numpy.float32(frame)
#    
#    # define criteria, number of clusters(K) and apply kmeans()
#    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#    K = 8
#    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
#    
#    # Now convert back into uint8, and make original image
#    center = numpy.uint8(center)
#    res = center[label.flatten()]
#    res2 = res.reshape((frame.shape))
#

    # TODO: Make dict for contour arrays and loop
    # only proceed if at least one contour was found
    if len(ctrs) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid'
        for ctr in ctrs:
            break
#        cB = max(cnts, key=cv2.contourArea)
#        approx = cv2.approxPolyDP(cB, 0.01 * cv2.arcLength(cB, True), True)
#
#        if len(approx) < 10:
#            x, y, w, h = cv2.boundingRect(cB)
#            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#        elif len(approx) > 10:
#            ((xB, yB), radiusB) = cv2.minEnclosingCircle(cB)
#            mB = cv2.moments(cB)
#            centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))
#
#            # only proceed if the radius meets a minimum size
#            if radiusB > 5:
#                # draw the circle and centroid on the frame,
#                # then update the list of tracked points
#                cv2.circle(frame, (int(xB), int(yB)), int(radiusB), (255, 0, 0), 2)
#                cv2.circle(frame, centerB, 5, (0, 0, 0), -1)
        while True:
            break

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
#    cv2.imshow("Image", img)
#    cv2.imshow("Kmeans", res2)
    cv2.imshow("Gray",gray)
    # if the 'q' key is pressed, stop the loop
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        break
=======
    bluelower = (96, 129, 149)
    blueupper = (116, 255, 255)

    greenlower = (54, 110, 118)
    greenupper = (76, 255, 255)

    yellowlower = (18, 78, 101)
    yellowupper = (36, 183, 255)

    redlower = (0, 36, 255)
    redupper = (13, 255, 255)

    while True:
        # grab the current frame
        frame = vs.read()

        # TODO: If above edited fix

        # handle the frame from VideoCapture or VideoStream
        frame = frame[1] if args.get("video", False) else frame

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break

        # resize the frame, blur it, and convert it to the gray
        # color space

        # TODO: maybe not resize or blur?
        frame = imutils.resize(frame, width=600)
        #blurred = cv2.GaussianBlur(frame, (5, 5), 0)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskb = cv2.inRange(hsv, bluelower, blueupper)
        maskg = cv2.inRange(hsv, greenlower, greenupper)
        maskr = cv2.inRange(hsv, redlower, redupper)
        masky = cv2.inRange(hsv, yellowlower, yellowupper)

        maskall = cv2.bitwise_or(maskb, maskg)
        maskall = cv2.bitwise_or(maskall, maskr)
        maskall = cv2.bitwise_or(maskall, maskr)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gray * maskall

        maskb = cv2.Canny(gray, 50, 100)
        # maskg = cv2.Canny(maskg, 50, 100)
        # maskr = cv2.Canny(maskr, 50, 100)
        # masky = cv2.Canny(masky, 50, 100)
        mask = cv2.Canny(maskall, 50, 100)

        # TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        centerB = None

        # TODO: Make dict for contour arrays and loop
        # only proceed if at least one contour was found
        # if len(cnts) > 0:
        #     # find the largest contour in the mask, then use
        #     # it to compute the minimum enclosing circle and
        #     # centroid
        #     cB = max(cnts, key=cv2.contourArea)
        #     approx = cv2.approxPolyDP(cB, 0.01 * cv2.arcLength(cB, True), True)
        #
        #     if len(approx) < 10:
        #         x, y, w, h = cv2.boundingRect(cB)
        #         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     elif len(approx) > 10:
        #         ((xB, yB), radiusB) = cv2.minEnclosingCircle(cB)
        #         mB = cv2.moments(cB)
        #         centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))
        #
        #         # only proceed if the radius meets a minimum size
        #         if radiusB > 5:
        #             # draw the circle and centroid on the frame,
        #             # then update the list of tracked points
        #             cv2.circle(frame, (int(xB), int(yB)), int(radiusB), (255, 0, 0), 2)
        #             cv2.circle(frame, centerB, 5, (0, 0, 0), -1)


        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", gray)
        #cv2.imshow("Blue", maskb)
        # cv2.imshow("Green", maskg)
        # cv2.imshow("Red", maskr)
        # cv2.imshow("Yellow", masky)


        # if the 'q' key is pressed, stop the loop
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break
>>>>>>> 5260c724b530e764e63d99257073e48c24688c8e

