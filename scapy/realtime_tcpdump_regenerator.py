# This script generate flow by tcpdump in day time

from scapy.all import *
from datetime import datetime
import sys

def main():
    if len(sys.argv) != 2:
        print "Usage : %s <tcpdump>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    packets = rdpcap(filename)
    print("read file completed")
    for packet in packets:
        while(1):
            current_time = datetime.now().strftime('%H:%M:%S')
            packet_time = datetime.fromtimestamp(packet.time).strftime('%H:%M:%S')
            print("current:" + current_time + "    packet_time:" + packet_time) 
            if (current_time == packet_time):
                print("BINGO!!!!!")
                break
            if (current_time > packet_time):
                break
        print("next")
        # if packet.haslayer("HTTPRequest"):
        # sendp(packet, iface="h0-eth0")
        # packet_time = datetime.fromtimestamp(packet.time).strftime('%H:%M:%S')
    print("SUCCESS")


if __name__ == "__main__":
    main()