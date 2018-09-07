
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

def main():
    datapath = "s0"
    while 1:
        lines = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-flows', datapath, '-O', 'OpenFlow13'])
        
        


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
        
        for line in lines:
            

            line = line.split(",")
            # print(line)

            # exception killing
            if (line[0][0:10] == "OFPST_FLOW"):
                continue
            if (line[5][0:9] == " priority"):
                continue


            if (line[6] == " priority=3"):
               
                duration = float(line[1][10:-1])
                packet_count = int(line[3][11:])
                byte_count = int(line[4][9:])
                src_IP = line[8][7:]
                dst_IP = line[9][7:]
                
                flow_IP = src_IP, dst_IP
                sorted_flow_IP = tuple(sorted(flow_IP))
                # print(sorted_flow_IP)

                # packetcount_list.append(packet_count)
                # bytescount_list.append(byte_count)
                # Pair_IP_hashlist.add(hash(sorted_flow_IP))
                # IP_hashlist.add(hash(flow_IP)) 

                # dst_IP_counter[dst_IP] += 1

                if (duration - window <= 0):
                    window_packetcount_list.append(packet_count)
                    window_bytescount_list.append(byte_count)
                    window_Pair_IP_hashlist.add(hash(sorted_flow_IP))
                    window_IP_hashlist.add(hash(flow_IP)) 
                    window_dst_IP_counter[dst_IP] += 1
                else:
                    packetcount_list.append(packet_count)
                    bytescount_list.append(byte_count)
                    Pair_IP_hashlist.add(hash(sorted_flow_IP))
                    IP_hashlist.add(hash(flow_IP)) 
                    dst_IP_counter[dst_IP] += 1


        packetcount = len(packetcount_list)
        if (packetcount != 0):
            mean_packetcount = mean(packetcount_list)
            mean_bytescount = mean(bytescount_list)
            median_packetcount = median(packetcount_list)
            median_bytescount = median(bytescount_list)
        else:
            mean_packetcount = 0
            mean_bytescount = 0
            median_packetcount = 0
            median_bytescount = 0
        

        window_packetcount = len(window_packetcount_list)
        if (window_packetcount != 0):
            window_mean_packetcount = mean(window_packetcount_list)
            window_mean_bytescount = mean(window_bytescount_list)
            window_median_packetcount = median(window_packetcount_list)
            window_median_bytescount = median(window_bytescount_list)
        else:
            window_mean_packetcount = 0
            window_mean_bytescount = 0
            window_median_packetcount = 0
            window_median_bytescount = 0

        if (len(IP_hashlist) != 0):
            Num_Pair_flows = len(IP_hashlist) - len(Pair_IP_hashlist)
            PPf = (2*Num_Pair_flows)/float(len(IP_hashlist))
        else:
            Num_Pair_flows = 0
            PPf = 0

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
            packet_count_ratio = 1
        else:
            packet_count_ratio = window_packetcount / float(packetcount)

        if (mean_packetcount == 0):
            packet_mean_ratio = 0
        else:
            packet_mean_ratio = window_mean_packetcount / mean_packetcount

        if (median_packetcount == 0):
            packet_median_ratio = 0
        else:
            packet_median_ratio = window_median_packetcount/median_packetcount

        if (mean_bytescount == 0):
            bytes_mean_ratio = 0
        else:
            bytes_mean_ratio = window_mean_bytescount/mean_bytescount

        if (median_bytescount == 0):
            bytes_median_ratio = 0
        else:
            bytes_median_ratio = window_median_bytescount/median_bytescount
            
        if (window_packetcount) != 0:
            dis_mean_packetcount = abs(mean_packetcount - window_mean_packetcount)
            dis_median_packetcount = abs(median_packetcount - window_median_packetcount)
            dis_mean_bytescount = abs(mean_bytescount - window_mean_bytescount)
            dis_median_bytescount = abs(median_bytescount - window_median_bytescount)
            dis_PPf = abs(PPf - windowPPf)
            dis_entropy = abs(entropy - window_entropy)
        else:
            dis_mean_packetcount = 0
            dis_median_packetcount = 0
            dis_mean_bytescount = 0
            dis_mean_bytescount = 0
            dis_median_bytescount = 0
            dis_PPf = 0
            dis_entropy = 0
        
        feature_list = []

        print("%65s" % "1. Packet count")
        print("%40s %40s" % ("all packet count: ", str(packetcount)))
        feature_list.append(packetcount)
        print("%40s %40s" % ("window's packet count: ", str(window_packetcount)))
        feature_list.append(window_packetcount)
        print("%40s %40s" % ("packet count ratio: ", str(packet_count_ratio)))
        feature_list.append(packet_count_ratio)

        print("%65s" % "2. Packet Mean & Median")
        print("%40s %40s" % ("mean of all packet count: ", str(mean_packetcount)))
        feature_list.append(mean_packetcount)
        print("%40s %40s" % ("mean of window's packet count: ", str(window_mean_packetcount)))
        feature_list.append(window_mean_packetcount)
        print("%40s %40s" % ("packet mean ratio: ", str(packet_mean_ratio)))
        feature_list.append(packet_mean_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_mean_packetcount)))
        feature_list.append(dis_mean_packetcount)
        print("%40s %40s" % ("median of all packet count: ", str(median_packetcount)))
        feature_list.append(median_packetcount)
        print("%40s %40s" % ("median of window's packet count: ", str(window_median_packetcount)))
        feature_list.append(window_median_packetcount)
        print("%40s %40s" % ("packet median ratio: ", str(packet_median_ratio)))
        feature_list.append(packet_median_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_median_packetcount)))
        feature_list.append(dis_median_packetcount)

        print("%65s" % "3. Bytes Mean & Median")
        print("%40s %40s" % ("mean of all bytes count: ", str(mean_bytescount)))
        feature_list.append(mean_bytescount)
        print("%40s %40s" % ("mean of window's bytes count: ", str(window_mean_bytescount)))
        feature_list.append(window_mean_bytescount)
        print("%40s %40s" % ("bytes mean ratio: ", str(bytes_mean_ratio)))
        feature_list.append(bytes_mean_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_mean_bytescount)))
        feature_list.append(dis_mean_bytescount)
        print("%40s %40s" % ("median of all bytes count: ", str(median_bytescount)))
        feature_list.append(median_bytescount)
        print("%40s %40s" % ("median of window's bytes count: ", str(window_median_bytescount)))
        feature_list.append(window_median_bytescount)
        print("%40s %40s" % ("bytes median ratio: ", str(bytes_median_ratio)))
        feature_list.append(bytes_median_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_median_bytescount)))
        feature_list.append(dis_median_bytescount)

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
        feature_list.append(Num_Pair_flows)
        print("%40s %40s" % ("flow: ", str(len(IP_hashlist))))
        feature_list.append(len(IP_hashlist))
        print("%40s %40s" % ("window's pair-flow: ", str(window_Num_Pair_flows)))
        feature_list.append(window_Num_Pair_flows)
        print("%40s %40s" % ("window's flow: ", str(len(window_IP_hashlist))))
        feature_list.append(len(window_IP_hashlist))
        print("%40s %40s" % ("percentage of all pair-flow: ", str(PPf)))
        feature_list.append(PPf)
        print("%40s %40s" % ("percentage of window's pair-flow: ", str(windowPPf)))
        feature_list.append(windowPPf)
        print("%40s %40s" % ("pair-flow ratio: ", str(PPf_ratio)))
        feature_list.append(PPf_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_PPf)))
        feature_list.append(dis_PPf)


        print("%65s" % "5. Entropy")
        # print("%40s %40s" % ("dst IP counter list: ", dstIP_counter_list))
        # print("%40s %40s" % ("window's dst IP counter list: ", window_dstIP_counter_list))
        print("%40s %40s" % ("entropy: ", entropy))
        feature_list.append(entropy)
        print("%40s %40s" % ("window's entropy: ", window_entropy))
        feature_list.append(window_entropy)
        print("%40s %40s" % ("entropy ratio: ", str(entropy_ratio)))
        feature_list.append(entropy_ratio)
        print("%40s %40s" % ("relative distance: ", str(dis_entropy)))
        feature_list.append(dis_entropy)

        print_buffer = ''.join( (str(e) + "\n") for e in feature_list)
        # print(print_buffer) 
        current_time = datetime.now().strftime('%m%d_%H%M%S')
        filename = "data/" + current_time            
        flow_table_log = open(filename, "w+")        
        flow_table_log.write(print_buffer)
        flow_table_log.close()

        time.sleep(10)



if __name__ ==  "__main__":
    main()