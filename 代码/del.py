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

for d in os.listdir('0'):
    p = '/home/sqWang/liuliang/needdel'
    d = os.path.join(p,d)
    pcaps = rdpcap(d)
    pasp = {}
    for p in pcaps:
        print(1)
        if p.haslayer("IP"):
            src_ip = p["IP"].src
            dst_ip = p["IP"].dst
            if p.haslayer("UDP"):
                sport = p["UDP"].sport
                dport = p["UDP"].dport
                udp_data = p["UDP"].payload.original
                if src_ip > dst_ip:  # order to unique
                    temp = dst_ip
                    dst_ip = src_ip
                    src_ip = temp
                if sport > dport:
                    temp = sport
                    sport = dport
                    dport = temp
                name = str(src_ip) + '_' + str(dst_ip) + '_' + str(sport) + '_' + str(dport)
                path = '/home/sqWang/liuliang/testUDP/0'
                mkdir_p(path)
                name = os.path.join(path, name)
                if (name) in pasp:
                    file = pasp[name]
                    file.write(udp_data)
                    pasp[name] = file
                else:
                    file = open(name + '.pcap', 'wb')
                    file.write(udp_data)
                    pasp[name] = file
            if p.haslayer("TCP"):
                sport = p["TCP"].sport
                dport = p["TCP"].dport
                if p.haslayer("Raw"):
                    tcp_data = p["Raw"].original  # in order to get payload without padding
                    if src_ip > dst_ip:
                        temp = dst_ip
                        dst_ip = src_ip
                        src_ip = temp
                    if sport > dport:
                        temp = sport
                        sport = dport
                        dport = temp
                    name = str(src_ip) + '_' + str(dst_ip) + '_' + str(sport) + '_' + str(dport)
                    path = '/home/sqWang/liuliang/testTCP/0'
                    mkdir_p(path)
                    name = os.path.join(path, name)
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






