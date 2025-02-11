import subprocess, re

def get_saved_wifi_profiles():
    wifi_profiles = {}

    try:
        # Get Wi-Fi profile names only
        output = subprocess.check_output(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"], encoding="utf-8")
        profile_names = [line.split(":")[0] for line in output.strip().split("\n") if "802-11-wireless" in line]

        if not profile_names:
            print("No Wi-Fi profiles found.")
            return wifi_profiles

        for profile in profile_names:
            try:
                profile_details = subprocess.check_output(["nmcli", "-s", "connection", "show", profile], encoding="utf-8")
                password_match = re.search(r"802-11-wireless-security.psk:\s*(.+)", profile_details)

                wifi_profiles[profile] = password_match.group(1) if password_match else "No password stored"

            except subprocess.CalledProcessError as e:
                wifi_profiles[profile] = f"Error retrieving details for {profile}: {e}"

    except FileNotFoundError:
        print("nmcli command not found. Make sure NetworkManager is installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error running nmcli command: {e}")

    return wifi_profiles

wifi_data = get_saved_wifi_profiles()
for wifi, password in wifi_data.items():
    print(f"SSID: {wifi}, Password: {password}")
