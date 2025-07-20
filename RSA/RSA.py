def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Larger RSA Key Setup
p = 61
q = 53
n = p * q              # 3233
phi_n = (p - 1) * (q - 1)  # 3120
e = 17
d = 2753

# Message to encrypt
plaintext = "Sardor19"
# Encrypt each character
encrypted = [mod_exp(ord(char), e, n) for char in plaintext]
# Decrypt each character
decrypted = ''.join([chr(mod_exp(char, d, n)) for char in encrypted])

print("Original message: ", plaintext)
print("Encrypted values:", encrypted)
print("Decrypted message:", decrypted)
