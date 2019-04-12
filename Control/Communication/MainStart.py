import subprocess
import time
import serial

#FIXME change serial port to correct port
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, writeTimeout = 10)

p = None

pushedGo = False
pushedStop = False

while(1):
	
	ser.isOpen()
	
	line = ser.readline()
	
	if (line == "G" and pushedGo == False):
		pushedStop = False
		pushedGo = True
		print('GO')
		p = subprocess.Popen(['python3', '~/Desktop/CAR/Vision/main/main.py']) #FIXME - double check file location
	elif (line == "S" and pushedStop == False):
		pushedGo = False
		pushedStop = True
		print('STOP')
		p.terminate()
		exit()
	
	time.sleep(0.1)
