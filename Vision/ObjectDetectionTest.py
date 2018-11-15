# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time


# TODO: Fix if needed due to no reference video being passed will always be webcam (speed on startup concerns)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
blueLower = (90, 105, 0)
blueUpper = (119, 255, 255)

greenLower = (52, 69, 0)
greenUpper = (78, 255, 255)

yellowLower = (19, 58, 157)
yellowUpper = (33, 255, 255)

redLower = (0, 95, 84)
redUpper = (18, 255, 255)

# TODO: Removes Arguments from buffer Im pretty sure?
pts = deque(maxlen=args["buffer"])




# TODO: Fix Below code if VideoStream is better at video capture reference to VideoStream class here :https://github.com/jrosebr1/imutils/blob/master/imutils/video/videostream.py


# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
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

    # resize the frame, blur it, and convert it to the HSV
    # color space
    
# TODO: maybe not resize or blur?
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for blue, green, yellow, and red, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    maskB = cv2.inRange(hsv, blueLower, blueUpper)
    maskB = cv2.erode(maskB, None, iterations=2)
    maskB = cv2.dilate(maskB, None, iterations=2)

    maskG = cv2.inRange(hsv, greenLower, greenUpper)
    maskG = cv2.erode(maskG, None, iterations=2)
    maskG = cv2.dilate(maskG, None, iterations=2)

    maskY = cv2.inRange(hsv, yellowLower, yellowUpper)
    maskY = cv2.erode(maskY, None, iterations=2)
    maskY = cv2.dilate(maskY, None, iterations=2)

    maskR = cv2.inRange(hsv, redLower, redUpper)
    maskR = cv2.erode(maskR, None, iterations=2)
    maskR = cv2.dilate(maskR, None, iterations=2)

# TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cntsB = cv2.findContours(maskB.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsB = cntsB[0] if imutils.is_cv2() else cntsB[1]
    centerB = None

    cntsG = cv2.findContours(maskG.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsG = cntsG[0] if imutils.is_cv2() else cntsG[1]
    centerG = None

    cntsY = cv2.findContours(maskY.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsY = cntsY[0] if imutils.is_cv2() else cntsY[1]
    centerY = None

    cntsR = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsR = cntsR[0] if imutils.is_cv2() else cntsR[1]
    centerR = None
# TODO: Make dict for contour arrays and loop
    # only proceed if at least one contour was found
    if len(cntsB) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cB = max(cntsB, key=cv2.contourArea)
        approx = cv2.approxPolyDP(cB, 0.01 * cv2.arcLength(cB, True), True)
        if len(approx) < 10:
            x, y, w, h = cv2.boundingRect(cB)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        elif len(approx) > 10:
            ((xB, yB), radiusB) = cv2.minEnclosingCircle(cB)
            mB = cv2.moments(cB)
            centerB = (int(mB["m10"] / mB["m00"]), int(mB["m01"] / mB["m00"]))

            # only proceed if the radius meets a minimum size
            if radiusB > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(xB), int(yB)), int(radiusB), (255, 0, 0), 2)
                cv2.circle(frame, centerB, 5, (0, 0, 0), -1)

    if len(cntsG) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cG = max(cntsG, key=cv2.contourArea)
        approx = cv2.approxPolyDP(cG, 0.01 * cv2.arcLength(cG, True), True)
        if len(approx) < 10:
            x, y, w, h = cv2.boundingRect(cG)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif len(approx) > 10:
            ((xG, yG), radiusG) = cv2.minEnclosingCircle(cG)
            mG = cv2.moments(cG)
            centerG = (int(mG["m10"] / mG["m00"]), int(mG["m01"] / mG["m00"]))

            # only proceed if the radius meets a minimum size
            if radiusG > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(xG), int(yG)), int(radiusG), (0, 255, 0), 2)
                cv2.circle(frame, centerG, 5, (0, 0, 0), -1)

    if len(cntsY) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cY = max(cntsY, key=cv2.contourArea)
        approx = cv2.approxPolyDP(cY, 0.01 * cv2.arcLength(cY, True), True)
        if len(approx) < 10:
            x, y, w, h = cv2.boundingRect(cY)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        elif len(approx) > 10:
            ((xY, yY), radiusY) = cv2.minEnclosingCircle(cY)
            mY = cv2.moments(cY)
            centerY = (int(mY["m10"] / mY["m00"]), int(mY["m01"] / mY["m00"]))

            # only proceed if the radius meets a minimum size
            if radiusY > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(xY), int(yY)), int(radiusY), (0, 255, 255), 2)
                cv2.circle(frame, centerY, 5, (0, 0, 0), -1)

    if len(cntsR) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cR = max(cntsR, key=cv2.contourArea)
        approx = cv2.approxPolyDP(cR, 0.01 * cv2.arcLength(cR, True), True)
        if len(approx) < 10:
            x, y, w, h = cv2.boundingRect(cR)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        elif len(approx) > 10:
            ((xR, yR), radiusR) = cv2.minEnclosingCircle(cR)
            mR = cv2.moments(cR)
            centerR = (int(mR["m10"] / mR["m00"]), int(mR["m01"] / mR["m00"]))

            # only proceed if the radius meets a minimum size
            if radiusR > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(xR), int(yR)), int(radiusR), (0, 0, 255), 2)
                cv2.circle(frame, centerR, 5, (0, 0, 0), -1)

    #cv2.imshow("Yellow", maskY)
    cv2.imshow("Frame", frame)

    # if the 'q' key is pressed, stop the loop
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
