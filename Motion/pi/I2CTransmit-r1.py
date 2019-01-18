#RPi Pinouts

#I2C Pins
#PI       Arduino
#GPIO2 -> A4
#GPIO3 -> A5
#Ground -> Ground

#On Arduino


#Import the Library Requreid 
import smbus
import time

bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x08

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def sendMessage(msg):
    data = msg
    data_list = list(data)

    for i in data_list:
        #Sends to the Slaves 
        writeNumber(int(ord(i)))
        time.sleep(.1)
    writeNumber(int(0x0A))

#Send a message to Arduino
while 1:
    sendMessage(raw_input("string to send:"))


#End of the Script
