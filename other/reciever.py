from scapy.all import sniff, UDP
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

def load_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def decrypt_message(private_key, encrypted_msg):
    try:
        decoded = base64.b64decode(encrypted_msg)
        original = private_key.decrypt(
            decoded,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def packet_handler(pkt):
    if pkt.haslayer(UDP) and pkt[UDP].dport == 5555:  # Match our port
        encrypted_msg = pkt[UDP].payload.load
        print(f"\nReceived encrypted message (base64): {encrypted_msg.decode()}")
        
        private_key = load_private_key()
        decrypted = decrypt_message(private_key, encrypted_msg)
        
        print(f"Decrypted message: {decrypted}")

def start_receiver():
    print("Starting receiver... Waiting for encrypted messages on port 5555")
    print("Press Ctrl+C to stop")
    sniff(filter="udp port 5555", prn=packet_handler, store=0)

if __name__ == "__main__":
    start_receiver()