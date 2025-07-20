from scapy.all import IP, UDP, send
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import base64

# The secret key (shared ahead of time)
key = b'8bytekey'

# Encrypt the message
cipher = DES.new(key, DES.MODE_ECB)
message = b"My secret message"
padded = pad(message, DES.block_size)
encrypted = cipher.encrypt(padded)

# Encode for safe transmission in the packet
payload = base64.b64encode(encrypted)

# Build and send UDP packet
ip = IP(dst="192.168.178.24")
udp = UDP(sport=4444, dport=5555)
pkt = ip/udp/payload
send(pkt)

print("Encrypted payload (Base64):", payload.decode())
