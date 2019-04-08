'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2


from movement import mov
from ColorFinder import findColor
from objFinder import objFind

if __name__ == "__main__":

    startTime = time.time()

    pickupEnd = startTime + 60 * 2  # 2 minutes

    dumpEnd = pickupEnd + 30  # 30 seconds to dump

    homeEnd = startTime + 60 * 3  # 3 minutes

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

    # Create the object finder
    objFind = objFind(capture)

    # Initialize Panduino communications
    mov = mov(w, h)

    # Send home color to Panduino
    mov.writeArray("h{0}".format(homeColor))

    try:
        while time.time() < pickupEnd:

            (food, tels) = objFind.findObjs()

            mov.whereToGo(food, tels)

            mov.goToWhere()

        while time.time() < dumpEnd:

            (pill, tels) = objFind.findObjs(food=False)

            mov.whereToGo(pill, tels)

            mov.gotToWhere()

        while time.time() < homeEnd:

            (pill, tels) = objFind.findObjs(food=False)

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
