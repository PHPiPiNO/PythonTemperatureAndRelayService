#!/usr/bin/env python
 
import sys, socket
from daemon import Daemon
 
class TemperatureAndRelayServiceDaemon(Daemon):
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.bind((socket.gethostname(), 7999))
        s.bind(('127.0.0.1', 7999))
        s.listen(1) # One connection at time is enough

        while True:
            (clientsocket, address) = s.accept()
            pckLen = clientsocket.recv(1)

            if len(packageLength) == 0:
                break

            pckLen = ord(pckLen)
            command = clientsocket.recv(pckLen)
            clientsocket.send('tutto bene!')
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
