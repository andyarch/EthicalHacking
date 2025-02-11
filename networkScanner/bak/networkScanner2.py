#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import sys
import ipaddress

# Functionality similar to "netdiscover -r 10.0.2.0/24"
# Alternate simplier method using:  scapy.arping(ip)

def get_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Scan network IP and MAC addresses.")
    parser.add_argument("-t", "--target", required=True, help="IP range in CIDR format (e.g., 192.168.1.0/24)")
    args = parser.parse_args()

    # Validate IP range
    if not validate_ip_range(args.target):
        print(
            f"[ERROR] Invalid IP range format: {args.target}. Please provide a valid CIDR format (e.g., 192.168.1.0/24).")
        sys.exit(1)

    return args


def validate_ip_range(ip_range):
    """
    Validates the provided IP range is in correct CIDR format.
    """
    try:
        ipaddress.ip_network(ip_range, strict=True)
        return True
    except ValueError:
        return False


def scan(ip_range):
    """
    Scans the network for active devices using ARP requests.
    """
    try:
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list, _ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    except Exception as e:
        print(f"[ERROR] Failed to scan network: {e}")
        sys.exit(1)

    machines_list = []
    for sent, received in answered_list:
        machines_list.append({"ip": received.psrc, "mac": received.hwsrc})

    return machines_list


def print_results(machines_list):
    """
    Prints the scan results in a formatted table.
    """
    if not machines_list:
        print("No active devices found on the network.")
        return

    print("\nNetwork Scan Results:")
    print("IP Address\t	MAC Address")
    print("----------------------------------------")
    for machine in machines_list:
        print(f"{machine['ip']}	{machine['mac']}")


if __name__ == "__main__":
    args = get_arguments()
    print("Scanning network... Please wait.")
    scan_results = scan(args.target)
    print_results(scan_results)
