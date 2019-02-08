'''

This is where the code for communicating to the movement arduino will go.

WSAD + Z followed by an int 0 to 255

W255 = FASTEST FORWARD PLZ
A255 = FASTEST LEFT PLZ (Turn on a dime)
S
D
Z0 = STOP

'''


import smbus2 as smbus
import time

bus = smbus.SMBus(1)

slave_address = 0x08

def writeArray(value):
    msg = []
    for x in value:
        msg.append(int(ord(x)))
    print(msg)
    bus.write_i2c_block_data(slave_address, 0, msg)
        #bus.write_byte_data(slave_address, 0, ord(x))
    return -1

writeArray('Hello World, my name is Matt')