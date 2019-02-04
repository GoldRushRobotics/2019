# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:06:15 2018

@author: Ziggy
"""

from cspaceSliders import FilterWindow
import cv2 as cv

capture = cv.VideoCapture(0)
ret, image = capture.read()
if(ret):
    window = FilterWindow('Filter Window', image)
while(True):
    ret, image = capture.read()
    if(ret):
        window.update(image)
        window.show(verbose=True)
        
        colorspace = window.colorspace
        lowerb, upperb = window.bounds
        mask = window.mask
        applied_mask = window.applied_mask
        
        print('Displaying the image with applied mask filtered in', colorspace,
              '\nwith lower bound', lowerb, 'and upper bound', upperb)
        cv.imshow('Applied Mask', applied_mask)
        cv.waitKey()
