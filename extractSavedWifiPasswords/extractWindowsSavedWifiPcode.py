#!usr/bin/env python3
import subprocess
import re

#Extract previously saved wifi ids and passwords on Windows, and return these in a dictionary data structure.

def get_saved_wifi_profiles():
    wifi_profiles = {}

    # Step 1: Get list of Wi-Fi profiles
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profile"], encoding="utf-8")
        profile_names = re.findall(r"All User Profile\s*:\s*(.+)", output)

        if not profile_names:
            print("No Wi-Fi profiles found.")
            return wifi_profiles

        # Step 2: Get passwords for each profile
        for profile in profile_names:
            try:
                profile_info = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"],
                                                       encoding="utf-8")
                password_match = re.search(r"Key Content\s*:\s*(.+)", profile_info)

                password = password_match.group(1) if password_match else None
                wifi_profiles[profile] = password if password else "No password stored"

            except subprocess.CalledProcessError:
                wifi_profiles[profile] = "Error retrieving details"

    except subprocess.CalledProcessError:
        print("Error running netsh command.")

    return wifi_profiles


# Run the function and print results
wifi_data = get_saved_wifi_profiles()
for wifi, password in wifi_data.items():
    print(f"SSID: {wifi}, Password: {password}")
