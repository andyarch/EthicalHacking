#!/usr/bin/env python3

import scapy.all as scapy
import subprocess
import argparse
import re
import sys


# Functionality similar to "netdiscover -r 10.0.2.0/24"

# Function to get command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Scan network IP and MAC addresses")
    parser.add_argument("-t", "--target", required=True, help="IP range in CIDR format")
    return parser.parse_args()


def scan(ip_range):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip_range)
    # arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False) #Timeout=1sec
    # print(answered_list.summary())

    machines_list = []
    for elements in answered_list:
        machine_dict = {"ip":elements[1].psrc, "mac":elements[1].hwsrc }
        machines_list.append(machine_dict)

    return machines_list

def print_results(machines_list):
    print("IP\t\tMAC\n------------------------------")
    for elements in machines_list:
        print(elements["ip"] + "\t" + elements["mac"])


args = get_arguments()

scan_results = scan(args.target) # "10.0.2.0/24"
print_results(scan_results)
