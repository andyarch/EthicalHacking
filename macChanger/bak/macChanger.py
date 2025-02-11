#!/usr/bin/env python3

import subprocess

#subprocess.call("echo $PATH", shell=True)
#subprocess.call("ifconfig", shell=True)

# subprocess.call("ifconfig enp0s3", shell=True)
# subprocess.call("ifconfig enp0s3 down", shell=True)
# subprocess.call("ifconfig enp0s3 hw ether 00:11:22:33:44:88", shell=True)
# subprocess.call("ifconfig enp0s3 up", shell=True)
# subprocess.call("ifconfig enp0s3", shell=True)


interface = input ("Which interface> ") # "enp0s3"
new_mac = input ("Enter new MAC> ") # "00:11:22:33:44:99"

print("Changing Mac address for interface " + interface + " to " + new_mac)

# shellCommand = ["ifconfig", interface]
shellCommand = "ifconfig " + interface
print("Executing> " + shellCommand)
subprocess.call(shellCommand)


shellCommand = "ifconfig " + interface + " down"
print("Executing> " + shellCommand)
subprocess.call(shellCommand, shell=True)

shellCommand = "ifconfig " + interface + " hw ether " + new_mac
print("Executing> " + shellCommand)
subprocess.call(shellCommand, shell=True)

shellCommand = "ifconfig " + interface + " up"
print("Executing> " + shellCommand)
subprocess.call(shellCommand, shell=True)

shellCommand = "ifconfig " + interface
print("Executing> " + shellCommand)
subprocess.call(shellCommand, shell=True)
