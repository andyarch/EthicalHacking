#!/usr/bin/env python3

import subprocess
import argparse

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
    print("Changing Mac address for interface " + interface + " to " + new_mac)

    shellCommand = ["ifconfig", interface]
    # print("Executing> ")
    # print(shellCommand)
    subprocess.call(shellCommand)

    shellCommand = ["ifconfig", interface, "down"]
    subprocess.call(shellCommand)

    shellCommand = ["ifconfig", interface, "hw", "ether", new_mac]
    subprocess.call(shellCommand)

    shellCommand = ["ifconfig", interface, "up"]
    subprocess.call(shellCommand)

    shellCommand = ["ifconfig", interface]
    subprocess.call(shellCommand)



args = get_arguments()
change_mac(args.interface, args.mac)
