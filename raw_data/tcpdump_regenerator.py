from scapy.all import *
from datetime import datetime
import sys
import subprocess
from datetime import datetime
from datetime import timedelta
import csv

def main():
    if len(sys.argv) != 2:
        print "Usage : %s <tcpdump>" % sys.argv[0]
        sys.exit(1)

    
    csvfile = open("./attacklog.csv", 'r')
    csvreader = csv.reader(csvfile)

    time_list = []
    for row in csvreader:
        time = datetime.strptime(row[2] + ':' + row[3], '%m/%d/%Y:%H:%M:%S').strftime('%m/%d/%Y_%H:%M:%S')
        time_list.append(time)
        time = datetime.strptime(row[2] + ':' + row[4], '%m/%d/%Y:%H:%M:%S').strftime('%m/%d/%Y_%H:%M:%S')
        time_list.append(time)
    print(time_list)
    time_list_index = 0



    filename = sys.argv[1]
    command = "find " + filename +" -iname 'new_file*' -printf \"%T@ %Tc %p\n\" | sort -n | awk '{print $7}'"
    paths = subprocess.check_output(command, shell=True).splitlines()
    
    # paths = '/home/laochanlam/git/DDoS_Experiment/darpa/training_data/week_3/wednesday/new_files22'
    print(paths)
    interval = 5
    interface = "h0-eth0"
    datapath = "s0"
    secsdelta = timedelta(seconds=interval)
    


    for i, path in enumerate(paths, start=0):
        packets = rdpcap(path)
        print("%d read pcap %s completed. time: %s" % (i, path, str(datetime.now())))


        for packet in packets:
            packet_time = datetime.fromtimestamp(packet.time).strftime('%m/%d/%Y_%H:%M:%S')
            if packet_time > time_list[time_list_index]:
                current_time = datetime.now().strftime('%m/%d/%Y_%H:%M:%S')
                time_file = open("data/time_point", "a+")
                time_file.write(time_list[time_list_index] + "\t" + current_time + "\n" )
                time_file.close()
                time_list_index = time_list_index + 1 
            if packet.haslayer(TCP) or packet.haslayer(UDP):
                sendp(packet, iface=interface, verbose=0)
        print("%d insert pcap %s completed. time: %s" % (i, path, str(datetime.now())))

    

    
if __name__ == "__main__":
    main()