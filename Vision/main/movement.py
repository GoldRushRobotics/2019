'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''


#import smbus2
import time


# port ttyS0 is the first serial port over wire and not cable. Will change




class mov:

    def __init__(self, w, h):
        #self.ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, writeTimeout=0)
        #self.bus = smbus2.SMBus(1)
        self.slave_address = 0x08

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
        msg = []
        for x in value:
            msg.append(int(ord(x)))
        print(msg)
        self.bus.write_i2c_block_data(self.slave_address, 0, msg)
            #bus.write_byte_data(slave_address, 0, ord(x))

    def whereToGo(self, x, y):

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

