from scapy.all import *
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

pcaps=rdpcap("facebook_chat_4b.pcap")
pasp = {}
for p in pcaps:
    if p.haslayer("IP"):
        src_ip = p["IP"].src
        dst_ip = p["IP"].dst
        if p.haslayer("UDP"):
            sport = p["UDP"].sport
            dport = p["UDP"].dport
            print(p["UDP"].payload.original)
        if p.haslayer("TCP"):
            sport = p["TCP"].sport
            dport = p["TCP"].dport






