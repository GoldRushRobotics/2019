'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2


from movement import mov
from ColorFinder import findColor
from objFinder import objFind

times = None
mov = None
finder = None


def setup():

    global times, mov, finder

    startTime = time.time()

    pickupEnd = startTime + 60 * 2  # 2 minutes

    dumpEnd = pickupEnd + 30  # 30 seconds to dump

    homeEnd = startTime + 60 * 3  # 3 minutes

    times = (startTime, pickupEnd, dumpEnd, homeEnd)

    # Setup the video stream
    capture = cv2.VideoCapture(0)

    # Get the width and height from the capture stream
    w = int(capture.get(3))
    h = int(capture.get(4))

    # Wait for camera to initialize
    time.sleep(2)

    # Grab the first frame
    ret, firstFrame = capture.read()

    # Calculate the home color from the first frame
    homeColor = findColor(firstFrame, 30, 30, (w / 2 + 30), h - 20)

    # Explicitly remove first frame to increase free space
    firstFrame.__del__()

    # Create the object finder
    finder = objFind(capture)

    # Initialize Panduino communications
    mov = mov(w, h)

    # Send home color to Panduino
    mov.writeArray("h{0}".format(homeColor))

if __name__ == "__main__":

    try:

        # Pickup foodstuffs
        while time.time() < times[1]:

            (food, tels) = finder.findObjs(food=True)

            mov.whereToGo(food, tels)

            mov.goToWhere()
        # Dump foodstuffs at  location
        while time.time() < dumpEnd[2]:

            (pill, tels) = finder.findObjs(food=False)

            mov.whereToGo(pill, tels)

            mov.gotToWhere()
        # Go home quickly
        while time.time() < homeEnd[3]:

            (pill, tels) = finder.findObjs(food=False, goHome=True)

            mov.whereToGo(pill, tels)

    except (KeyboardInterrupt, ValueError) as e:

        # If there is a keyboard interrupt, tell Panduino to stop
        mov.writeArray('a0')
        mov.writeArray('w0')
        mov.writeArray('z0')

        # Destroy all cv2 windows
        cv2.destroyAllWindows()

        # Close the serial connection
        mov.ser.close()

        # Exit python
        exit()
