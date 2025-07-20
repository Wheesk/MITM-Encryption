from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

plaintext = b"Hello Sardor"
key = b"Sixteen byte key"  # 16 bytes key for AES-128
cipher = AES.new(key, AES.MODE_CBC)
iv = cipher.iv
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
print("Plaintext:", plaintext)
print("Ciphertext (hex): ", ciphertext.hex())
print("IV (hex): ", iv.hex())

# Decryption
cipher2 = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher2.decrypt(ciphertext), AES.block_size)
print("Decrypted:", decrypted)
