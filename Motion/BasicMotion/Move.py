import time
import serial

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, writeTimeout = 0)

ser.isOpen()

ser.write("w20".encode())
print('forward')
print('w20'.encode())
time.sleep(2)
ser.write('a30'.encode())
print('left')
time.sleep(2)
ser.write('s20'.encode())
print('back')
time.sleep(2)
ser.write('d30'.encode())
print('right')
time.sleep(2)
ser.write('z0'.encode())
print('stop')

ser.close()
