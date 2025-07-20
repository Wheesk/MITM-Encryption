from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

plaintext = b"Hello Sardor!"
key = b"8bytekey"  # 8 bytes key for DES
cipher = DES.new(key, DES.MODE_CBC)
iv = cipher.iv
ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))
print("Plaintext: ", plaintext)
print("Ciphertext (hex): ", ciphertext.hex())
print("IV (hex): ", iv.hex())

# Decryption
cipher2 = DES.new(key, DES.MODE_CBC, iv)
decrypted = unpad(cipher2.decrypt(ciphertext), DES.block_size)
print("Decrypted: ", decrypted)
