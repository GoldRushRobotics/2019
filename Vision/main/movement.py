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
# ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, writeTimeout=0)
# bus = smbus2.SMBus(1)
#
# slave_address = 0x08

# def writeArray(value):
#     msg = []
#     for x in value:
#         msg.append(int(ord(x)))
#     print(msg)
#     bus.write_i2c_block_data(slave_address, 0, msg)
#         #bus.write_byte_data(slave_address, 0, ord(x))
#     return -1

def chasefood(x, y):
    # if (x < 450) and (x > 150):
    #     direction = 'w'
    #     if y < 300:
    #         speed = ((y * -1) + 600) / 5
    #     elif y >= 300:
    #         speed = y / 5
    # elif x < 150:
    #     direction = 'a'
    #     if y < 300:
    #         speed = ((y * -1) + 600) / 50
    #     elif y >= 300:
    #         speed = y / 50
    # elif x > 450:
    #     direction = 'd'
    #     if y < 300:
    #         speed = ((y * -1) + 600) / 50
    #     elif y >= 300:
    #         speed = y / 50
    #
    # move = direction + str(int(speed))

    #x direction and speed
    xdirec = 'a0'
    if (x >= 0) and (x < 100):
        xdirec = 'a150'

    if (x > 100) and (x < 200):
        xdirec = 'a100'

    if (x > 200) and (x < 300):
        xdirec = 'a50'

    if (x > 300) and (x < 400):
        xdirec = 'd50'

    if (x > 400) and (x < 500):
        xdirec = 'd100'

    if (x > 500) and (x <= 600):
        xdirec = 'd150'

    #y direction and speed
    ydirec = 'w0'
    if (y >= 0) and (y < 100):
        ydirec = 'w50'

    if (y > 100) and (y < 200):
        ydirec = 'w50'

    if (y > 200) and (y < 300):
        ydirec = 'w75'

    if (y > 300) and (y < 400):
        ydirec = 'w100'

    if (y > 400) and (y < 500):
        ydirec = 'd50'

    if (y > 500) and (y <= 600):
        ydirec = 'd50'


    return ydirec, xdirec

