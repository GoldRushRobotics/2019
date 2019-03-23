'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2


from movement import mov
from FindMyHome import home
from objFinder import foodFinder, telsFinder

if __name__ == "__main__":


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
    homeColor = home(firstFrame, w, h)

    # Create the object finders
    foodFind = foodFinder(capture, w, h)
    telsFind = telsFinder(capture, w, h)
    #pillFind = pillFinder(capture, w, h)

    # Initialize Panduino communications
    mov = mov(w, h)

    # Send home color to Panduino
    mov.writeArray("h{0}".format(homeColor))

    try:
        while 1:

            (food, tels) = (foodFind.findFood(), telsFind.findTel())

            mov.whereToGo(food, tels)

            mov.goToWhere()

    except KeyboardInterrupt:

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




