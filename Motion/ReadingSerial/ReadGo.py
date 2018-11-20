#4th down -> Rx
#5th down -> Tx

import serial

ser = serial.Serial(port='/dev/ttyS0', baudrate = 9600)

input = b'0'
while input != b'1':
    input = ser.read()

print('Go!')
