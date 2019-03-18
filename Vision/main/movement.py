'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

h + {rgby} to set home color

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''

import time
#import serial
import math



class mov:

    def __init__(self, w, h):
        #self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, writeTimeout = 0)

        self.w = w
        self.halfW = w/2
        self.h = h
        self.gravConst = 1.0

    def mapVal(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return int(rightMin + (valueScaled * rightSpan))

    def writeArray(self, value):

        print(value)

        # Uncomment below when actually running
        #self.ser.isOpen()
        #self.ser.write(value.encode())

    def goToWhere(self):
        for i in self.values:
             self.writeArray(i)
             time.sleep(.001)

    def findTurn(self, objLoc, objgrav):

        totalturn = 0
        for obj in objLoc:
            x, y = obj


            if x == -1 or y == -1:
                return 0, False

#        if (x < self.halfW):
#            xsqr = -((x-self.halfW)/self.halfW *(x-self.halfW)/self.halfW)
#        else:
#            xsqr = (x-self.halfW)/self.halfW * (x-self.halfW)/self.halfW
#
#        ysqr = y/self.h * y/self.h
#
#        turn = xsqr * ysqr * objgrav * self.gravConst

            turn = ((x-self.halfW)/self.halfW) * ((self.h-y)/self.h) * self.gravConst * objgrav
            totalturn += turn
        #return (turn, 1-abs(turn))
        if(len(objLoc) == 0):
            return 0, True
        return totalturn/len(objLoc), True

    def whereToGo(self, food, tels):

        foodDirection, foodEx = self.findTurn(food,1.0)
        telDirection, telEx = self.findTurn(tels,-.75)

        if telEx and foodEx:
            numObj = 2
        elif telEx or foodEx:
            numObj = 1
        else:
            self.values = ['w0','a0'] #TODO this cant do nothing
            return

        direction = foodDirection + telDirection#to keep under 1.0 may need mods

        if direction < 0:
            mappedVal = int((-255 * direction)/numObj)

            xdirec = "a{}".format(mappedVal)
        else:
            mappedVal = int((255 * direction)/numObj)

            xdirec = "d{}".format(mappedVal)

        ydirec = "w{0}".format(int(255*(1-abs(direction))))

        self.values = [ydirec,xdirec]
        return(ydirec, xdirec)


if __name__ == "__main__":
    m = mov(600,600)
    #print(m.whereToGo([(100, 100), (300, 300)], [(100,100)])[0])
    print(m.whereToGo([(200, 200)], []))

        # if x != -1 & y != -1:
        #     #x direction
        #     xdirec = 'a0'
        #     if (x <= self.halfW):
        #         m = self.mapVal(x,0,self.halfW,255,0)
        #         xdirec = 'a{0}'.format(m)

        #     else:
        #         m = self.mapVal(x,self.halfW,self.w,0,255)
        #         xdirec = 'd{0}'.format(m)

        #     #y speed
        #     ydirec = 'w0'
        #     ydirec = "w{0}".format(self.mapVal(y,0,self.h,0,128))

        #     self.values = [ydirec,xdirec]
        # else:
        #     self.values = ['w0','a0']
#