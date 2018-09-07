from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types 
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import arp
from ryu.lib import hub
import json

from collections import Counter
from math import log
from numpy import median
from numpy import mean

class Controller(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {} 
        self.monitor_thread = hub.spawn(self._monitor)
        self.packets_per_flow_list = []



    # SwitchFeatures packet handler
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        # Add default flow
        self.add_flow(datapath, 0, 0, match, actions)

        # let UDP through controller 
        # match = parser.OFPMatch(eth_type=0x0800, ip_proto=0x11)
        # self.add_flow(datapath, 2, match, actions)
        

    # StateChange packet handler
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    # FlowStatsReply packet handler
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        self.logger.info("This is %016x EventOFPFlowStatsReply.", ev.msg.datapath.id)
        # self.logger.info('%s', json.dumps(ev.msg.to_jsondict(), ensure_ascii=True,
        # 								  indent=3, sort_keys=True))

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

        for stat in sorted([flow for flow in body if (flow.priority == 3)]):
                
        # self.logger.info('%s', json.dumps(ev.msg.to_jsondict(), ensure_ascii=True, indent=3, sort_keys=True))
            
            # print(stat)
            duration = stat.duration_nsec / 1000000000.0 + stat.duration_sec
            

            # extract Pair_flows here
            flow_IP = stat.match['ipv4_dst'],  stat.match['ipv4_src'] 
            sorted_flow_IP = tuple(sorted(flow_IP))
            dst_IP = stat.match['ipv4_dst']

            packetcount_list.append(stat.packet_count)
            bytescount_list.append(stat.byte_count)
            Pair_IP_hashlist.add(hash(sorted_flow_IP))
            IP_hashlist.add(hash(flow_IP)) 

            dst_IP_counter[dst_IP] += 1
            
            # within window 
            if (duration - window <= 0):
                window_packetcount_list.append(stat.packet_count)
                window_bytescount_list.append(stat.byte_count)
                window_Pair_IP_hashlist.add(hash(sorted_flow_IP))
                window_IP_hashlist.add(hash(flow_IP)) 
                window_dst_IP_counter[dst_IP] += 1

        packetcount = len(packetcount_list)
        mean_packetcount = mean(packetcount_list)
        mean_bytescount = mean(bytescount_list)
        Num_Pair_flows = len(IP_hashlist) - len(Pair_IP_hashlist)
        PPf = (2*Num_Pair_flows)/float(len(IP_hashlist))

        window_packetcount = len(window_packetcount_list)
        window_mean_packetcount = mean(window_packetcount_list)
        window_mean_bytescount = mean(window_bytescount_list)
        window_Num_Pair_flows = len(window_IP_hashlist) - len(window_Pair_IP_hashlist)
        windowPPf = (2*window_Num_Pair_flows)/float(len(window_IP_hashlist))

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

        self.logger.info("%65s" % "1. Packet count")
        self.logger.info("%40s %40s" % ("all packet count: ", str(packetcount)))
        self.logger.info("%40s %40s" % ("window's packet count: ", str(window_packetcount)))
        self.logger.info("%40s %40s" % ("packet count ratio: ", str(window_packetcount/float(packetcount))))

        self.logger.info("%65s" % "2. Packet Mean")
        self.logger.info("%40s %40s" % ("mean of all packet count: ", str(mean_packetcount)))
        self.logger.info("%40s %40s" % ("mean of window's packet count: ", str(window_mean_packetcount)))
        self.logger.info("%40s %40s" % ("mean ratio: ", str(window_mean_packetcount/mean_packetcount)))

        self.logger.info("%65s" % "3. Bytes Mean")
        self.logger.info("%40s %40s" % ("mean of all bytes count: ", str(mean_bytescount)))
        self.logger.info("%40s %40s" % ("mean of window's bytes count: ", str(window_mean_bytescount)))
        self.logger.info("%40s %40s" % ("mean ratio: ", str(window_mean_bytescount/mean_bytescount)))

        self.logger.info("%65s" % "4. Percentage of Pair-Flow")
        self.logger.info("%40s %40s" % ("pair-flow: ", str(Num_Pair_flows)))
        self.logger.info("%40s %40s" % ("flow: ", str(len(IP_hashlist))))
        self.logger.info("%40s %40s" % ("window's pair-flow: ", str(window_Num_Pair_flows)))
        self.logger.info("%40s %40s" % ("window's flow: ", str(len(window_IP_hashlist))))
        self.logger.info("%40s %40s" % ("percentage of all pair-flow: ", str(PPf)))
        self.logger.info("%40s %40s" % ("percentage of window's pair-flow: ", str( windowPPf)))
        self.logger.info("%40s %40s" % ("pair-flow ratio: ", str(windowPPf/PPf)))

        self.logger.info("%65s" % "5. Entropy")
        self.logger.info("%40s %40s" % ("dst IP counter list: ", dstIP_counter_list))
        self.logger.info("%40s %40s" % ("window's dst IP counter list: ", window_dstIP_counter_list))
        self.logger.info("%40s %40s" % ("entropy: ", entropy))
        self.logger.info("%40s %40s" % ("window's entropy: ", window_entropy))
        self.logger.info("%40s %40s" % ("entropy ratio: ", window_entropy/entropy))
        # for stat in sorted([flow for flow in body if flow.priority == 1],
        #                key=lambda flow: (flow.match['in_port'],
        #                                  flow.match['eth_dst'])):
        #     self.logger.info('%016x %8x %17s %8x %8d %8d',
        # 					ev.msg.datapath.id,
        # 					stat.match['in_port'], stat.match['eth_dst'],
        # 					stat.instructions[0].actions[0].port,
        # 					stat.packet_count, stat.byte_count)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        # self.logger.info("This is %016x EventOFPPortStateReply.", ev.msg.datapath.id)

        

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        self.logger.debug("send stats request: %016x", datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # send FlowStatsRequest & PortStatsRequest packet to switch(datapath)
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)


    def add_flow(self, datapath, priority, idle_timeout, match, actions, buffer_id=None):
        ofproto = datapath.ofproto  
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        # self.logger.info("\n#########Add flow #########")
        # self.logger.info(match)
        # self.logger.info("###########################\n")
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, idle_timeout=idle_timeout,
                                    match=match, instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, idle_timeout=idle_timeout, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        # If you hit this you might want to increase
        # the "miss_send_length" of your switch

        # ev is the Openflow isntance 
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
    
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        # print(eth.ethertype)

        # print("THIS PACKET IS:")
        # print("layer 3 protocol")
        # print(pkt_ipv4)
        # print("layer 2 protocol")
        # self.logger.info(eth)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            # self.logger.info('ETH_TYPE_LLDP in\n')
            return  
        if eth.ethertype == ether_types.ETH_TYPE_IPV6:
            # ignore ipv6 packet
            # self.logger.info('ETH_TYPE_IPV6 in\n')
            return

        # print("###################################################################")
        # self.logger.info(pkt)
        # self.logger.info(self.mac_to_port)
        dst = eth.dst
        src = eth.src
        data = msg.data
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # self.logger.info(self.mac_to_port)

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        # self.logger.info(out_port)
        # self.logger.info("THIS PACKET CONTAIN:")
        # for p in pkt.protocols:
        #     self.logger.info(1)


        # if UDP packet_in into controller
        if pkt.get_protocol(udp.udp):
            pkt_layer4 = pkt.get_protocol(udp.udp)
            pkt_layer3 = pkt.get_protocol(ipv4.ipv4)
            layer4_srcport = pkt_layer4.src_port
            layer4_dstport = pkt_layer4.dst_port
            layer3_srcip = pkt_layer3.src
            layer3_dstip = pkt_layer3.dst
            match = parser.OFPMatch(ipv4_src=layer3_srcip, ipv4_dst=layer3_dstip, 
                                    eth_type=0x0800, ip_proto=0x11, 
                                    udp_src=layer4_srcport, udp_dst=layer4_dstport)
            actions = [parser.OFPActionOutput(out_port)]
            idle_timeout = 300
            self.add_flow(datapath, 3, idle_timeout, match, actions)
            # TODO: Buffer id understanding
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER,
                                        in_port=in_port, actions=actions, data=data)
            datapath.send_msg(out)
            return

        # if tcp packet_in into controller
        if pkt.get_protocol(tcp.tcp):
            pkt_layer4 = pkt.get_protocol(tcp.tcp)
            pkt_layer3 = pkt.get_protocol(ipv4.ipv4)
            layer4_srcport = pkt_layer4.src_port
            layer4_dstport = pkt_layer4.dst_port
            layer3_srcip = pkt_layer3.src
            layer3_dstip = pkt_layer3.dst
            # self.logger.info(layer4_srcport)
            # self.logger.info(layer4_dstport)
            # self.logger.info(layer3_srcip)
            # self.logger.info(layer3_dstip)
            match = parser.OFPMatch(ipv4_src=layer3_srcip, ipv4_dst=layer3_dstip, 
                                    eth_type=0x0800, ip_proto=0x06, 
                                    tcp_src=layer4_srcport, tcp_dst=layer4_dstport)
            actions = [parser.OFPActionOutput(out_port)]
            idle_timeout = 300
            self.add_flow(datapath, 3, idle_timeout, match, actions)
            # TODO: Buffer id understanding
            out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER,
                                        in_port=in_port, actions=actions, data=data)
            datapath.send_msg(out)
            return

        #         # TODO: Buffer id understanding
        #         out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER,
        #                                 in_port=in_port, actions=actions, data=data)


        # default routing (ARP)
        # actions = [parser.OFPActionOutput(out_port)]
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
        #     # self.logger.info("ADD AGAIN? + return")
        #     self.add_flow(datapath, 1, match, actions)

        # # construct packet_out message and send it.
        # out = parser.OFPPacketOut(datapath=datapath,
        #                         buffer_id=ofproto.OFP_NO_BUFFER,
        #                         in_port=in_port, actions=actions,
        #                         data=msg.data)
        # self.logger.info("SEND!!!!!!!!")
        # datapath.send_msg(out)
