import serial
import sys

try:
  value = sys.argv[1]
except:
  value = "f0"

ser = serial.Serial(
    port='/dev/ttyACM0', baudrate=115200, writeTimeout=0)
#value = "f0"
print(value)

# Uncomment below when actually running
ser.isOpen()
ser.write(value.encode())
