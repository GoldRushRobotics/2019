# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import argparse
import cv2
import imutils
import time


# TODO: Fix if needed due to no reference video being passed will always be webcam (speed on startup concerns)

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
      vs = VideoStream(src=0).start()

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


def loop(vs,args):
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
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # mask = cv2.inRange(gray, blueLower, blueUpper)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.Canny(gray, 50, 100)

    # TODO: Remove center initialization code(No point to waste memory here) also again with the videostream
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    centerB = None

    # TODO: Make dict for contour arrays and loop
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cB = max(cnts, key=cv2.contourArea)
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


    cv2.imshow("Frame", frame)

    # if the 'q' key is pressed, stop the loop
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        break





if __name__ == "__main__":

  vs,args = setup()

  time.sleep(2.0)

  loop(vs,args)

  death(vs,args)

