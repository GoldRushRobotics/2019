#RPi Pinouts

#I2C Pins
#GPIO2 -> SDA
#GPIO3 -> SCL

#Import the Library Requreid
import smbus2 as smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04


def writeNumber(value):
    bus.write_byte(address, value)


x = []
for n in range(10):
    x.appned[n]

print(x)

#End of the Script

