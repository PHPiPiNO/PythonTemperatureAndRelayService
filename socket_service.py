#!/usr/bin/env python

"""
The following code is mainly based on the code found in this article:
https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

by Sander Marechal - @Prezent - https://github.com/sandermarechal

And in this article:
http://raspberrypirobot.blogspot.it/2012/10/socket-communications-php-to-python.html
"""
 
import sys, socket, serial, time
from daemon import Daemon
 
class TemperatureAndRelayServiceDaemon(Daemon):
    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        ser.timeout=2
        time.sleep(2)

        # Read the System ready string
        ser.readline()

        #s.bind((socket.gethostname(), 7999))
        soc.bind(('127.0.0.1', 7999))
        soc.listen(1) # One connection at time is enough

        while True:
            (clientsocket, address) = soc.accept()

            # We aspect to receive a one character length command:
            command = str(clientsocket.recv(1))

            # Let's see if the serial is still open
            if(ser.isOpen() == False):
                ser.open()
                time.sleep(1)

            ser.write(command)
            time.sleep(0.3)
            res = ser.readline().rstrip()

            # Send the response length
            clientsocket.send(chr(len(res)))
            # Send the response
            clientsocket.send(res)
            clientsocket.close()

if __name__ == "__main__":
    daemon = TemperatureAndRelayServiceDaemon('/tmp/tr-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
