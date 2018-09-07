
from scapy.all import *
from datetime import datetime
import sys
import subprocess
from datetime import datetime
from datetime import timedelta
from collections import Counter
from math import log
from numpy import median
from numpy import mean


def data_analysis(lines):

    lines = lines.splitlines()
    packetcount_list = []
    bytescount_list = []
    dst_IP_counter = Counter()
    Pair_IP_hashlist = set()
    IP_hashlist = set()

    # window = 10s
    window = 10
    window_packetcount_list = []
    window_bytescount_list = []
    window_dst_IP_counter = Counter()
    window_Pair_IP_hashlist = set()
    window_IP_hashlist = set()

    dstIP_probability_list = []
    window_dstIP_probability_list = []
    entropy_list = []
    window_entropy_list = []

    # # n_packets
    for line in lines:
        line = line.split(",")
        # print(line)
        if (line[0][0:10] == "OFPST_FLOW"):
            continue
        if (line[5] == " priority=3"):
            # print(1)
            duration = float(line[1][10:-1])
            packet_count = int(line[3][11:])
            byte_count = int(line[4][9:])
            src_IP = line[7][7:]
            dst_IP = line[8][7:]


            flow_IP = src_IP, dst_IP
            sorted_flow_IP = tuple(sorted(flow_IP))
            print(sorted_flow_IP)

            packetcount_list.append(packet_count)
            bytescount_list.append(byte_count)
            Pair_IP_hashlist.add(hash(sorted_flow_IP))
            IP_hashlist.add(hash(flow_IP)) 

            dst_IP_counter[dst_IP] += 1

            if (duration - window <= 0):
                window_packetcount_list.append(stat.packet_count)
                window_bytescount_list.append(stat.byte_count)
                window_Pair_IP_hashlist.add(hash(sorted_flow_IP))
                window_IP_hashlist.add(hash(flow_IP)) 
                window_dst_IP_counter[dst_IP] += 1


    packetcount = len(packetcount_list)
    if (packetcount != 0):
        mean_packetcount = mean(packetcount_list)
        mean_bytescount = mean(bytescount_list)
    else:
        mean_packetcount = 0
        mean_bytescount = 0
    
    if (len(IP_hashlist) != 0):
        Num_Pair_flows = len(IP_hashlist) - len(Pair_IP_hashlist)
        PPf = (2*Num_Pair_flows)/float(len(IP_hashlist))
    else:
        Num_Pair_flows = 0
        PPf = 0

    window_packetcount = len(window_packetcount_list)
    if (window_packetcount != 0):
        window_mean_packetcount = mean(window_packetcount_list)
        window_mean_bytescount = mean(window_bytescount_list)
    else:
        window_mean_packetcount = 0
        window_mean_bytescount = 0

    if (len(window_IP_hashlist) != 0):
        window_Num_Pair_flows = len(window_IP_hashlist) - len(window_Pair_IP_hashlist)
        windowPPf = (2*window_Num_Pair_flows)/float(len(window_IP_hashlist))
    else:
        window_Num_Pair_flows = 0
        windowPPf = 0

    # entropy
    dstIP_counter_list = dst_IP_counter.values()
    for value in dstIP_counter_list:
        dstIP_probability_list.append(value/float(packetcount))
    window_dstIP_counter_list = window_dst_IP_counter.values()
    for value in window_dstIP_counter_list:
        window_dstIP_probability_list.append(value/float(window_packetcount))

    for value in dstIP_probability_list:
        entropy_list.append(value * log(value, 2))
    for value in window_dstIP_probability_list:
        window_entropy_list.append(value * log(value, 2))
    entropy = -sum(entropy_list)
    window_entropy = -sum(window_entropy_list)

    if (packetcount == 0):
        packet_count_ratio = 0
    else:
        packet_count_ratio = (window_packetcount/float(packetcount))

    if (mean_packetcount == 0):
        mean_ratio = 0
    else:
        mean_ratio = window_mean_packetcount/mean_packetcount

    if (mean_bytescount == 0):
        mean_ratio = 0
    else:
        mean_ratio = window_mean_bytescount/mean_bytescount
        
    print("%65s" % "1. Packet count")
    print("%40s %40s" % ("all packet count: ", str(packetcount)))
    print("%40s %40s" % ("window's packet count: ", str(window_packetcount)))
    print("%40s %40s" % ("packet count ratio: ", str(packet_count_ratio)))

    print("%65s" % "2. Packet Mean")
    print("%40s %40s" % ("mean of all packet count: ", str(mean_packetcount)))
    print("%40s %40s" % ("mean of window's packet count: ", str(window_mean_packetcount)))
    print("%40s %40s" % ("packet mean ratio: ", str(mean_ratio)))

    print("%65s" % "3. Bytes Mean")
    print("%40s %40s" % ("mean of all bytes count: ", str(mean_bytescount)))
    print("%40s %40s" % ("mean of window's bytes count: ", str(window_mean_bytescount)))
    print("%40s %40s" % ("bytes mean ratio: ", str(mean_ratio)))

    if (PPf != 0):
        PPf_ratio = windowPPf/PPf
    else:
        PPf_ratio = 0

    if (entropy != 0):
        entropy_ratio = window_entropy/entropy
    else:
        entropy_ratio = 0
        
    print("%65s" % "4. Percentage of Pair-Flow")
    print("%40s %40s" % ("pair-flow: ", str(Num_Pair_flows)))
    print("%40s %40s" % ("flow: ", str(len(IP_hashlist))))
    print("%40s %40s" % ("window's pair-flow: ", str(window_Num_Pair_flows)))
    print("%40s %40s" % ("window's flow: ", str(len(window_IP_hashlist))))
    print("%40s %40s" % ("percentage of all pair-flow: ", str(PPf)))
    print("%40s %40s" % ("percentage of window's pair-flow: ", str( windowPPf)))
    print("%40s %40s" % ("pair-flow ratio: ", str(PPf_ratio)))

    print("%65s" % "5. Entropy")
    print("%40s %40s" % ("dst IP counter list: ", dstIP_counter_list))
    print("%40s %40s" % ("window's dst IP counter list: ", window_dstIP_counter_list))
    print("%40s %40s" % ("entropy: ", entropy))
    print("%40s %40s" % ("window's entropy: ", window_entropy))
    print("%40s %40s" % ("entropy ratio: ", str(entropy_ratio)))


def main():
    if len(sys.argv) != 2:
        print "Usage : %s <tcpdump>" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    command = "find " + filename +" -iname 'new_file*' -printf \"%T@ %Tc %p\n\" | sort -n | awk '{print $7}'"
    paths = subprocess.check_output(command, shell=True).splitlines()
    print(paths)

    interval = 10
    interface = "h0-eth0"
    datapath = "s0"
    secsdelta = timedelta(seconds=interval)

    for i, path in enumerate(paths, start=0):
        packets = rdpcap(path)
        print("%d read pcap %s completed." % (i, path))

        # the first iteration
        if (i == 0):
            # init timestamp
            interval_timestamp = datetime.fromtimestamp(packets[0].time)
            #.strftime('%Y-%m-%d_%H-%M-%S')
            print("start with: " + interval_timestamp.strftime('%Y-%m-%d_%H-%M-%S'))
            interval_timestamp = interval_timestamp + secsdelta
            # print(interval_timestamp.strftime('%Y-%m-%d_%H-%M-%S'))
    
        for packet in packets:
            packet_timestamp = datetime.fromtimestamp(packet.time)
            if packet_timestamp < interval_timestamp:
                # print(packet_timestamp.strftime('%Y-%m-%d_%H-%M-%S'))
                # specify interface
                sendp(packet, iface=interface, verbose=0)
            else:
                print("[PRINT FLOW TABLE] %s" % interval_timestamp)
                line = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-flows', datapath, '-O', 'OpenFlow13'])
                filename = packet_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
                print(packet_timestamp.strftime('%Y-%m-%d_%H-%M-%S'))
                
                data_analysis(line)
                # filename = "data/" + filename            
                # flow_table_log = open(filename, "w")        
                # flow_table_log.write(line[2:])
                # flow_table_log.close()

                interval_timestamp = interval_timestamp + secsdelta
                print("Add 10 secs")
                print(packet_timestamp.strftime('%Y-%m-%d_%H-%M-%S'))
                sendp(packet, iface=interface, verbose=0)

    #print(packet_timestamp)
#    datapath = "s0"    
#    line = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-flows', datapath, '-O', 'OpenFlow13'])
#    current_time = datetime.now().strftime('%H:%M:%S')

#    print(current_time)


# def find_all(name, path):
#     reselt = []
#     for root, dirs, files in os.walk(path):
#         if name in files:
#             result.append(os.path.join(root, name))
#     return result
    
if __name__ == "__main__":
    main()
