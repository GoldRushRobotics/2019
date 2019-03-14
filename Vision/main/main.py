'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2


from movement import mov
import FindMyHome as home
from objFinder import foodFinder

if __name__ == "__main__":


    # Setup the video stream
    capture = cv2.VideoCapture(0)

    # Get the width and height from the capture stream
    w = int(captrue.get(3))
    h = int(capture.get(4))

    # Wait for camera to initialize
    time.sleep(2)

    # Grab the first frame
    ret, firstFrame = capture.read()

    # Calculate the home color from the first frame
    homeColor = home(firstFrame, w, h)

    # Create the object finders
    food = foodFinder(capture, w, h)
    tels = telsFinder(capture, w, h)
    pill = pillFinder(capture, w, h)

    # Initialize Panduino communications
    mov = mov(w, h)

    # Send home color to Panduino
    mov.writeArray("h{0}".format(homeColor))

    try:
        while 1:
                x,y = finder.findFood()

                mov.whereToGo(x,y)

                mov.goToWhere()

                print(mov.values)

    except KeyboardInterrupt:

        # If there is a keyboard interrupt, tell Panduino to stop
        mov.writeArray('a0')
        mov.writeArray('w0')

        # Close the serial connection
        mov.ser.close()

        # Destroy all cv2 windows
        cv2.destroyAllWindows()

        # Exit python
        exit()




