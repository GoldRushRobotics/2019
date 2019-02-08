import time
import serial

ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, writeTimeout = 0)

ser.isOpen()

ser.write("w50".encode())
print('forward')
time.sleep(2)

ser.write('a70'.encode())
print('left')
time.sleep(2)

ser.write('s50'.encode())
print('back')
time.sleep(2)

ser.write('d70'.encode())
print('right')
time.sleep(2)

ser.write('z0'.encode())
print('stop')

ser.close()
