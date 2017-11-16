#!/usr/bin/env python
 
import socket, serial, time
 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.timeout=2
time.sleep(2)

print "Ready to start!"

# Read the System ready string
ser.readline()

soc.bind(('127.0.0.1', 7999))
soc.listen(1) # One connection at time is enough

while True:
    (clientsocket, address) = soc.accept()
    # We aspect to receive a one character length command:
    command = str(clientsocket.recv(1))

    print "Ricevuto il comando: "+command

    ser.write(command)
    time.sleep(0.3)
    res = ser.readline().rstrip()



    # Send the response length
    clientsocket.send(chr(len(res)))
    # Send the response
    clientsocket.send(res)
    clientsocket.close()
