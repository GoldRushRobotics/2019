'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''

import time
import serial


class mov:

    def __init__(self, w, h):
        self.ser = None #serial.Serial(port='/dev/ttyACM0', baudrate=115200, writeTimeout = 0)

        self.w = w
        self.halfW = w/2
        self.h = h

    def mapVal(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(rightMin + (valueScaled * rightSpan))

    def writeArray(self, value):
        self.ser.isOpen()
        self.ser.write(value.encode())

    def gotToWhere(self):
        for i in self.values:
             self.writeArray(i)
             time.sleep(.001)

    def whereToGo(self, x, y):

        if x != -1 & y != -1:
            #x direction and speed
            xdirec = 'a0'
            if (x <= self.halfW):
                m = self.mapVal(x,0,self.halfW,255,0)
                xdirec = 'a{0}'.format(m)

            else:
                m = self.mapVal(x,self.halfW,self.w,0,255)
                xdirec = 'd{0}'.format(m)

            #y direction and speed
            ydirec = 'w0'
            ydirec = "w{0}".format(self.mapVal(y,0,self.h,0,255))

            self.values = [ydirec,xdirec]
        else:
            self.values = ['w0','a0']


    def __del__(self):
        self.ser.close()

