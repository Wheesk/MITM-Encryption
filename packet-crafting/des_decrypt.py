from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import base64

# The same secret key
key = b'8bytekey'

# Suppose this is the payload you copied from Wireshark (as bytes)
received_payload = b'cLQBCAXOlhseJiV41JvByzOS4taoBwFR'  

# Decode from base64
encrypted = base64.b64decode(received_payload)

# Decrypt
cipher = DES.new(key, DES.MODE_ECB)
decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)
print("Decrypted message:", decrypted.decode())
