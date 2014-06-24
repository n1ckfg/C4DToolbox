import c4d, math, sys
import socket, time, threading
from random import uniform as rnd

#~~~~~~~~~~~~~~~~~~
from c4dtoolbox import *
#~~~~~~~~~~~~~~~~~~

# Based on https://github.com/jusu/Cinema4D-Helpers

#
# Udp
#

class Script:
    def __init__(self, name):
        self.name = name

        nth = self.readNth()
        nth += 1
        self.initialValue = nth
        self.writeNth(nth)

    def writeNth(self, n):
        try:
            f = open("/tmp/_c4d_nth" + self.name, "w")
            f.write(str(n))
            f.close()
        except IOError:
            print "Failed to write nth."

    def readNth(self):
        try:
            f = open("/tmp/_c4d_nth" + self.name)
            n = int(f.readline())
            f.close()
            return n
        except IOError:
            return 0

    def IsCurrent(self):
        return self.initialValue == self.readNth()

class Udp:
    HOST = 'localhost'
    bufsize = 1024
    timeout = 0.5

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((Udp.HOST, port))
        self.sock.settimeout(Udp.timeout)

    def read(self):
        try:
            data, addr = self.sock.recvfrom(Udp.bufsize)
        except socket.timeout:
            data = None
            pass
        
        return data

    def close(self):
        self.sock.close()

def listen(name, port, handlers):
    """Listen to udp port, handle data with 'handlers'
    (dictionary of prefix-function values).

    Name: unique string.
    """

    scr = Script(name)

    def task():
        # wait to release socket
        time.sleep(1)

        udp = Udp(port)

        while scr.IsCurrent():
            data = udp.read()
            if data:
                p = data.partition(' ')

                try:
                    handlers[p[0]](p[2])
                except KeyError:
                    pass

        udp.close()

    t = threading.Thread(target=task)
    t.start()
