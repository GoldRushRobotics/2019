'''

This is where the code for communicating to the movement arduino will go.

<<<<<<< HEAD
WSAD + Z followed by an int 0 to 255

W
A
S
D
Z0 = STOP

'''


import smbus as smbus
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
=======
'''
>>>>>>> 5260c724b530e764e63d99257073e48c24688c8e
