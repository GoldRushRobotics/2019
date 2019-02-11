'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''


import smbus2
import time

bus = smbus2.SMBus(1)

slave_address = 0x08

# def writeArray(value):
#     msg = []
#     for x in value:
#         msg.append(int(ord(x)))
#     print(msg)
#     bus.write_i2c_block_data(slave_address, 0, msg)
#         #bus.write_byte_data(slave_address, 0, ord(x))
#     return -1

def chasefood(x, y):
    speed = 0
    if(y < 100):
        speed = 50
    elif((y > 100) and (y < 200)):
        speed = 75
    elif((y > 200) and (y < 300)):
        speed = 100
    elif((y > 300) and (y < 400)):
        speed = 125
    elif((y > 400) and (y < 500)):
        speed = 150
    elif(y > 500):
        speed = 150

    return x, speed
