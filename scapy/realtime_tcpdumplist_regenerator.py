#!/usr/bin/env python
# This script generate flow by tcpdumplist in day time

import sys
from datetime import datetime
from scapy.all import *

def main():
    if len(sys.argv) != 2:
        print "Usage : %s <tcpdump.list>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as f:
        file = f.read().splitlines()

    for line in file:
        line = line.split()
        #only look for HTTP packet
        while(1):
            current_time = datetime.now().strftime('%H:%M:%S')
            # print("current:" + current_time + "    line[2]:" + line[2]) 
            if (current_time == line[2]):
                print("BINGO!!!!!")
                break
            if (current_time > line[2]):
                break 
        print("next")
        if (line[4] == "http"):
            print(line[4])

if __name__ == "__main__":
    main()