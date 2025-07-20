from scapy.all import IP, UDP, send
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64

# Step 1: Generate RSA Key Pair (would normally be done once and keys saved)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Step 2: Encrypt with RSA Public Key
def rsa_encrypt(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted)  # Base64 for safe packet inclusion
# Step 3: Decrypt with RSA Private Key (for receiver)
def rsa_decrypt(private_key, encrypted_msg):
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
# Generate keys (in real use, receiver would have their own private key)
private_key, public_key = generate_rsa_keys()

# Original message
original_msg = "Hello, this is me!"
print(f"Original: {original_msg}")

# Encrypt the message
encrypted_msg = rsa_encrypt(public_key, original_msg)
print(f"Encrypted: {encrypted_msg}")

# Build packet
ip = IP(src="10.112.41.132", dst="10.112.41.125")
udp = UDP(sport=12345, dport=80)
pkt = ip/udp/encrypted_msg

# Show and send
pkt.show()
send(pkt, verbose=0)

# Simulate decryption at receiver (normally on different machine)
print("\nSimulating receiver decryption...")
decrypted = rsa_decrypt(private_key, encrypted_msg)
print(f"Decrypted: {decrypted}")