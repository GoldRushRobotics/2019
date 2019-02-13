'''

This is the main function. EVERYTHING should be called from here. This should be the only python thingy running on game day.


'''

import time
import cv2
# import movement as mov
import FindMyHome as home
# import FindMeContours as cont
from objFinder import foodFinder

if __name__ == "__main__":

  # real = cv2.VideoCapture(0)
  trails = cv2.VideoCapture("all_Balls.JPG")
  finder = foodFinder(trails)

  x,y = finder.findFood()

  print(x,y)

  #homeColor = home.findHomeColor()




