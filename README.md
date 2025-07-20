## ARP Spoofing MITM — Network Hacking Adventure
Welcome to my cyber-lab!
This repo is all about discovering, experimenting, and documenting what really happens when you combine Python, Scapy, Wireshark, and a dash of curiosity on a local network.

If you’ve ever wondered “how do hackers actually pull off a man-in-the-middle attack?”—this is your step-by-step, screenshot-rich answer.

---

## Introduction 
Have you ever read about MITM attacks and thought, “That sounds complicated”?
I used to think so, too—until I built one from scratch, watched the packets fly in Wireshark, and realized it’s equal parts science and sorcery.

This project covers:

Encrypting messages with DES, AES, and RSA (because attackers and defenders both need crypto!).

Crafting and sending packets using Scapy.

Launching a real ARP spoofing attack to become the “invisible router” on my LAN.

Analyzing everything in Wireshark, with real screenshots and commentary.

---

## Lab Setup
Attacker: Kali Linux VM (bridged mode), Python 3, Scapy, Wireshark

Victim: Ubuntu VM on the same LAN

Gateway: Standard home router

Network Interface: eth0

<img src="images/config.jpg" width="300"/>

---

## Encryption Playground
Before diving into attacks, I wanted to see how classic and modern encryption actually works at the byte level.

AES Encryption and Decryption (with CBC Mode)
Step-by-step explanation:
1.	We create a 16-byte secret key for AES.
2.	We create a cipher object for encryption (using CBC mode, which is secure).
3.	The code pads the message to the correct length, then encrypts it.
4.	The code prints out the encrypted data and the special IV (Initialization Vector) needed to decrypt.
5.	To decrypt, we use the same key and IV, and the code prints the decrypted message.

<img src="images/aes.jpg" width="300"/>

DES Encryption and Decryption (with CBC Mode)
Step-by-step explanation:
1.	We create an 8-byte secret key for DES.
2.	We set up the DES cipher object for encryption (also in CBC mode).
3.	The message is padded, encrypted, and the result plus IV are printed out.
4.	For decryption, the same key and IV are used, and the decrypted message is shown

<img src="images/des.jpg" width="300"/>
Scripts in /aes_des/ encrypt and decrypt a sample message.

Comparasion table: 

<img src="images/table.jpg" width="300"/>

RSA Encryption: 
Step 1: Set up the keys
•	We pick two large prime numbers, p and q.
•	Calculate n = p * q (the modulus for both keys).
•	Calculate phi_n = (p-1)*(q-1) (used in key calculations).
•	Choose a public exponent e (commonly 17, 65537, etc.).
•	Calculate the private exponent d, which is used for decryption.
Step 2: Encrypt the message
•	For each character in the message, get its Unicode number (ord(char)).
•	Encrypt that number with the formula:
encrypted_char = (char_number ^ e) mod n
•	This is done for each character and stored as a list.
Step 3: Decrypt the message
•	For each encrypted number, apply the formula:
decrypted_char = (encrypted_number ^ d) mod n
•	Convert back to the character using chr().

<img src="images/rsa.jpg" width="300"/>

--- 

## Packet Crafting 101
What if you could send your own message—encrypted or not—right onto the wire?
With Scapy, I crafted custom UDP packets, stuffed in a DES-encrypted payload, and watched them hit the LAN.

- How to run:
- See /packet-crafting/.
- Edit the IPs, run as root, and capture in Wireshark.

For this demonstration, I set the key directly in my code (hardcoded):
key = b'8bytekey'
- This key is 8 bytes long, which is required for DES.

- I used the same key in both the sender and receiver scripts, so that both can encrypt and decrypt messages

•	This key is 8 bytes long, which is required for DES.
•	I used the same key in both the sender and receiver scripts, so that both can encrypt and decrypt messages

•	This key is 8 bytes long, which is required for DES.
•	I used the same key in both the sender and receiver scripts, so that both can encrypt and decrypt messages

1) Encrypting the packet payload(sender script)

<img src="images/encrypt.jpg" width="300"/>

Wireshark: 

<img src="images/wireshark.jpg" width="300"/>

2) Decrypting the Packet Payload (Receiver Script)

<img src="images/decrypt.jpg" width="300"/>