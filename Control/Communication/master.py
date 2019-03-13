import subprocess
import time
import serial

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, writeTimeout = 10)

p = None

pushedGo = False
pushedStop = False

while(1):
	
	ser.isOpen()
	
	line = ser.readline()
	
	if (line == b'G\n' and pushedGo == False):
		pushedStop = False
		pushedGo = True
		print('GO')
		p = subprocess.Popen(['python3', 'slave.py'])
	elif (line == b'S\n' and pushedStop == False):
		pushedGo = False
		pushedStop = True
		print('STOP')
		p.terminate()
		exit()
	
	time.sleep(0.1)
