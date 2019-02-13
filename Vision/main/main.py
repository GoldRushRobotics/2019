'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2
import movement as mov
import FindMyHome as home
# import FindMeContours as cont
from objFinder import foodFinder

if __name__ == "__main__":

  # real = cv2.VideoCapture(0)
  trials = cv2.VideoCapture("all_Balls.JPG")
  finder = foodFinder(trials)

  x,y = finder.findFood()

  codes = mov.whereToGo(x,y,finder.width,finder.height)

  #homeColor = home.findHomeColor()




