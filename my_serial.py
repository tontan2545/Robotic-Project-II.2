import serial
import time
import json

ser = serial.Serial('/dev/ttyACM0', 115200)
print(ser.name)

while True:
    for i in range(4):
        message = b"{\"dir\":%d}"%i
        print(message)
        ser.write(message)
        time.sleep(2)
    for i in range(4,0,-1):
        message = b"{\"dir\":%d}"%i
        print(message)
        ser.write(message)
        time.sleep(2)
    

