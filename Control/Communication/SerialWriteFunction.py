import serial

#port ttyS0 is the first serial port over wire and not cable. Will change
ser = serial.Serial(port='/dev/ttyS0', baudrate=115200, writeTimeout = 0)

def cmd(msg):
	ser.isOpen()
	ser.write(msg.encode())
	
#at end it is good to close serial connection
ser.close()