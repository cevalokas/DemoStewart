import serial
import time
ser = serial.Serial('COM4', 115200, 8, 'N', 1)
   
# Send character 'S' to start the program
#self.USBPort = serial.Serial('COM4', 115200, 8, 'N', 1)

ser.write(bytes(b'\x01\x00\x01\x01'))
ser.write(b'\x01\x00\x01\x01')
