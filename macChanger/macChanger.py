#!/usr/bin/env python3

import subprocess
import argparse
import re
import sys

# Core functionality
# subprocess.call("ifconfig enp0s3 down", shell=True)
# subprocess.call("ifconfig enp0s3 hw ether 00:11:22:33:44:88", shell=True)
# subprocess.call("ifconfig enp0s3 up", shell=True)

# Function to get command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Change MAC address of a network interface")
    parser.add_argument("-i", "--interface", required=True, help="Interface to change MAC address")
    parser.add_argument("-m", "--mac", required=True, help="New MAC address (format: XX:XX:XX:XX:XX:XX)")
    return parser.parse_args()

# Function to validate MAC address format
def is_valid_mac(mac):
    return bool(re.match(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$", mac))

# Function to get the current MAC address of an interface
def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface], stderr=subprocess.STDOUT).decode()
        mac_address_match = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)
        return mac_address_match.group(0) if mac_address_match else None
    except FileNotFoundError:
        print("Error: 'ifconfig' command not found. Please install net-tools (sudo apt install net-tools).")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"Error: Interface '{interface}' not found. Please check the interface name.")
        sys.exit(1)

# Function to change the MAC address
def change_mac(interface, new_mac):
    try:
        print(f"[INFO] Changing MAC address of {interface} to {new_mac}...")
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print("[SUCCESS] MAC address changed successfully.")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to change MAC address for {interface}. Ensure you have root privileges.")
        sys.exit(1)

# Main execution
if __name__ == "__main__":
    args = get_arguments()

    # Validate MAC address format
    if not is_valid_mac(args.mac):
        print(f"[ERROR] Invalid MAC address format: {args.mac}. Use format XX:XX:XX:XX:XX:XX")
        sys.exit(1)

    current_mac = get_current_mac(args.interface)
    if current_mac:
        print(f"Current MAC Address: {current_mac}")
    else:
        print(f"[ERROR] Unable to retrieve MAC address for interface '{args.interface}'")
        sys.exit(1)

    # Check if the new MAC is the same as the current one
    if current_mac == args.mac:
        print("[INFO] The new MAC address is the same as the current one. No changes made.")
    else:
        change_mac(args.interface, args.mac)
        updated_mac = get_current_mac(args.interface)

        if updated_mac == args.mac:
            print(f"[SUCCESS] MAC address updated successfully to {updated_mac}")
        else:
            print("[ERROR] MAC address change failed.")
