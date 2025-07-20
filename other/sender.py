from scapy.all import IP, UDP, send
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

def load_public_key():
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted)

def send_spoofed_message(dst_ip, dst_port, message, spoof_ip):
    public_key = load_public_key()
    encrypted_msg = encrypt_message(public_key, message)
    
    print(f"Original message: {message}")
    print(f"Encrypted message: {encrypted_msg.decode()}")
    print(f"Spoofing source IP as: {spoof_ip}")
    
    # Build packet with SPOOFED source IP
    ip = IP(src=spoof_ip, dst=dst_ip)
    udp = UDP(dport=dst_port)
    pkt = ip/udp/encrypted_msg
    
    print("\nSpoofed packet details:")
    pkt.show()
    
    send(pkt, verbose=0)
    print(f"\nSent spoofed encrypted message from {spoof_ip} to {dst_ip}:{dst_port}")

if __name__ == "__main__":
    
    TARGET_IP = "10.112.41.125"  
    TARGET_PORT = 80
    MESSAGE = "This is a spoofed message with custom IP"
    SPOOF_IP = "10.112.41.132"   
    
    send_spoofed_message(TARGET_IP, TARGET_PORT, MESSAGE, SPOOF_IP)