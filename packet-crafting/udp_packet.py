from scapy.all import IP, UDP, send

packet = IP(dst="192.168.178.28")/UDP(dport=5555, sport=4444)/b"Hello, this is a test!"
send(packet)
