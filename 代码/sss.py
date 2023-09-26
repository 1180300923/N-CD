
import scapy
from scapy.all import *
from scapy.utils import PcapReader
from scapy.all import *
import os

pcaps=rdpcap("tt.pcap")
pasp = {}
for p in pcaps:
    if p.haslayer("IP"):
        src_ip = p["IP"].src
        dst_ip = p["IP"].dst
        if p.haslayer("UDP"):
            sport = p["UDP"].sport
            dport = p["UDP"].dport
            if p.haslayer("UDP"):
                tcp_data = p["UDP"].payload.original
                print(tcp_data)
                if src_ip > dst_ip:
                    temp = dst_ip
                    dst_ip = src_ip
                    src_ip = temp
                if sport > dport:
                    temp = sport
                    sport = dport
                    dport = temp
                name = str(src_ip) + '_' + str(dst_ip) + '_' + str(sport) + '_' + str(dport)
                if (name) in pasp:
                    file = pasp[name]
                    file.write(tcp_data)
                    pasp[name] = file
                else:
                    file = open(name + '.pcap', 'wb')
                    file.write(tcp_data)
                    pasp[name] = file
for file in pasp.values():
    file.close()