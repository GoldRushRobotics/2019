import cv2
import random
import sys


img = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
print(type(img))
print(img.shape)
