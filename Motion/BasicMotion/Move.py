import smbus2 as smbus
import time

bus = smbus.SMBus(1)

slave_address = 0x04

def writeNumber(value):
    bus.write_byte(slave_address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def sendMessage(msg):
    data = msg
    data_list = list(data)

    for i in data_list:
        # Sends to the Slaves
        writeNumber(int(ord(i)))
        time.sleep(.1)
    writeNumber(int(0x0A))

#loop (4)
#drive forward
#turn left

#turn 180

#loop (4)
#drive forward
#turn right
