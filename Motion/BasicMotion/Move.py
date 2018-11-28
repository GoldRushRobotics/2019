import smbus as smbus
import time

bus = smbus.SMBus(1)

slave_address = 0x08

def writeArray(value):
    bus.write_i2c_block_data(slave_address, 0, value)
    return -1

#while 1:
writeArray([ord('w'),200,1])
time.sleep(3)

writeArray([ord('f'),0,127])
#time.sleep(5)