#! /usr/bin/python3

import logging
from scapy.all import *
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

src_ip = "192.168.1.84"

def tcp_connect_scan(dst_ip):
    dst_port = 8000
    src_port = RandShort()
    tcp_connect_scan_result = sr1(IP(src = src_ip, dst = dst_ip)/TCP(sport = src_port, dport = dst_port), timeout = 50)
    print(type(tcp_connect_scan_result))

    if str(type(tcp_connect_scan_result)) == "<class 'NoneType'>":
        print("BE FILTERED.")
    elif tcp_connect_scan_result.haslayer(TCP):
        #if SYN_ACK
        if tcp_connect_scan_result.getlayer(TCP).flags == 0x12:
            send_ack_rst = sr(IP(dst = dst_ip, src = src_ip)/TCP(sport = src_port, dport = dst_port, flags= "AR"), timeout = 10)
            print("OPEN")
        elif tcp_connect_scan_result.getlayer(TCP).flags == 0x14:
            print("CLOSED")
    else:
        print("BE FILTERED.")
    print("finish tcp connect scan.")
   

def tcp_syn_scan(dst_ip):
  
    dst_port = 8000
    src_port = RandShort()
    tcp_connect_scan_result = sr1(IP(src = src_ip, dst = dst_ip)/TCP(sport = src_port, dport = dst_port), timeout = 50)
    print(type(tcp_connect_scan_result))

    if str(type(tcp_connect_scan_result)) == "<class 'NoneType'>":
        print("BE FILTERED.")
    elif tcp_connect_scan_result.haslayer(TCP):
        #if SYN_ACK
        if tcp_connect_scan_result.getlayer(TCP).flags == 0x12:
            send_ack_rst = sr(IP(dst = dst_ip, src = src_ip)/TCP(sport = src_port, dport = dst_port, flags= "R"), timeout = 10)
            print("OPEN")
        elif tcp_connect_scan_result.getlayer(TCP).flags == 0x14:
            print("CLOSED")
    else:
        print("BE FILTERED.")
    print("finish tcp connect scan.")
  


def tcp_xmas_scan(dst_ip):
    dst_port = 8000
    src_port = RandShort()
    xmas_scan_resp = sr1(IP(dst=dst_ip) / TCP(dport=dst_port, flags="FPU"), timeout=10)
    print(type(xmas_scan_resp))

    if (str(type(xmas_scan_resp)) == "<class 'NoneType'>"):
        print("Open|Filtered")

    elif (xmas_scan_resp.haslayer(TCP)):
        if (xmas_scan_resp.getlayer(TCP).flags == 0x14):
            print("Closed")
    elif (xmas_scan_resp.haslayer(ICMP)):
        if (int(xmas_scan_resp.getlayer(ICMP).type) == 3 and int(xmas_scan_resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10,13]):
            print("Filtered")
    print('finished tcp xmas scan.\n')


def tcp_fin_scan(dst_ip):
    src_port = RandShort()
    dst_port = 8000

    fin_scan_resp = sr1(IP(dst=dst_ip) / TCP(dport=dst_port, flags="F"), timeout=10)
    print(type(fin_scan_resp))

    if (str(type(fin_scan_resp)) == "<class 'NoneType'>"):
        print("Open|Filtered")
    elif (fin_scan_resp.haslayer(TCP)):
        if (fin_scan_resp.getlayer(TCP).flags == 0x14):
            print("Closed")

    elif (fin_scan_resp.haslayer(ICMP)):
        if (int(fin_scan_resp.getlayer(ICMP).type) == 3 and int(fin_scan_resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10,13]):
            print("Filtered")
    print('finished tcp fin scan.\n')



def tcp_null_scan(dst_ip):
    src_port = RandShort()
    dst_port = 8000

    null_scan_resp = sr1(IP(dst=dst_ip) / TCP(dport=dst_port, flags=""), timeout=10)
    print(type(null_scan_resp))

    if (str(type(null_scan_resp)) == "<class 'NoneType'>"):
        print("Open|Filtered")

    elif (null_scan_resp.haslayer(TCP)):
        if (null_scan_resp.getlayer(TCP).flags == 0x14):
            print("Closed")
    elif (null_scan_resp.haslayer(ICMP)):
        if (int(null_scan_resp.getlayer(ICMP).type) == 3 and int(null_scan_resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10,13]):
            print("Filtered")

    print('finished tcp null scan.\n')


def udp_scan(dst_ip):
    dst_port = 53
    dst_timeout = 10
    udp_scan_resp = sr1(IP(dst = dst_ip)/UDP(dport = dst_port), timeout = dst_timeout)
    print(type(udp_scan_resp))

    if (udp_scan_resp is None):
        print("OPEN|FILTERED")
    elif (udp_scan_resp.haslayer(UDP)):
        print("OPEN")
    elif(udp_scan_resp.haslayer(ICMP)): 
        if(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code) == 3):
            print("CLOSED")
        elif(int(udp_scan_resp.getlayer(ICMP).type)==3 and int(udp_scan_resp.getlayer(ICMP).code) in [1,2,9,10,13]):
            print('FILTERED')
        elif(udp_scan_resp.haslayer(IP) and udp_scan_resp.getlayer(IP).proto == IP_PROTOS.udp):
            print("OPEN")
    print('finish udp scan.\n')


if __name__ == '__main__':
    dst_ip = "192.168.1.1"

   # print("tcp connect scan...")
   # tcp_connect_scan(dst_ip)

   # print("tcp syn scan...")
   # tcp_syn_scan(dst_ip)
   # print('tcp xmas scan......')
   # tcp_xmas_scan(dst_ip)

  #  print('tcp fin scan......')
  #  tcp_fin_scan(dst_ip)

  #  print('tcp null scan......')
  #  tcp_null_scan(dst_ip)
    
    print('udp scan......')
    udp_scan(dst_ip)
