
import cv2
import time
import math


def objPoop(height, width, color, x, y):
    turn = 'z'
    dump = 'e'

    if color == 'g' or color == 'r':  # turn left, dump right
        turn = 'a'
        dump = 'r'

    elif color == 'y' or color == 'b':  # turn right, dump left
        turn = 'd'
        dump = 'l'

    if x != -1:  # while x is defined
        return ("w0 {0}25".format(turn)), "z0 p{0}".format(dump)), False
    else:
        return ("w0 {0}25".format(turn), "z0 p{0}".format(dump)), True
