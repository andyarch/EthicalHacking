#!/usr/bin/env python3

import subprocess
import argparse
import re

# subprocess.call("ifconfig enp0s3 down", shell=True)
# subprocess.call("ifconfig enp0s3 hw ether 00:11:22:33:44:88", shell=True)
# subprocess.call("ifconfig enp0s3 up", shell=True)

# Get command line arguments
def get_arguments():
    # Create an ArgumentParser instance
    parser = argparse.ArgumentParser(description="Change MAC address of a network interface")

    # Define command-line arguments
    parser.add_argument("-i", "--interface", required=True, help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", required=True, help="New MAC address")

    # Parse the arguments
    args = parser.parse_args()

    # Extract values
    # interface = args.interface # "enp0s3"
    # new_mac = args.mac # "00:11:22:33:44:99"

    return args


# Change the MAC address
def change_mac(interface, new_mac):
    # print("Changing Mac address for interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    try:
        ifconfig_results = subprocess.check_output(["ifconfig", args.interface], stderr=subprocess.STDOUT)
        search_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_results))

        if search_results:
            return search_results.group(0)
        else:
            print("MAC Address not found in ifconfig output.")

    except FileNotFoundError:
        print("Error: 'ifconfig' command not found. Ensure net-tools is installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to retrieve interface details. {e.output.decode('utf-8').strip()}")
    except Exception as e:
        print(f"Unexpected error: {e}")


args = get_arguments()
current_mac = get_current_mac(args.interface)
print("Current MAC: " + str(current_mac))
if current_mac == args.mac:
    print("New MAC address is the same as current. No change made")
else:
    change_mac(args.interface, args.mac)
    updated_mac = get_current_mac(args.interface)
    if updated_mac == args.mac:
        print("MAC was updated to:" + updated_mac)
    else:
        print("MAC could not be updated")

