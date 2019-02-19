'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2
from movement import mov
import FindMyHome as home
# import FindMeContours as cont
from objFinder import foodFinder

if __name__ == "__main__":

    # real = cv2.VideoCapture(0)
    trials = cv2.VideoCapture(0)

    finder = foodFinder(trials)

    mov = mov(finder.width, finder.height)

    while 1:
        try:
            x,y = finder.findFood()

            mov.whereToGo(x,y)

            print(mov.values)
        except:
            print("blah")

        #for i in codes:
            #mov.writeArray(i)

    #homeColor = home.findHomeColor()




