import socket

# Define RDP pod details
POD_IPS = [
    "172.20.13.68",
"172.20.57.195",
"172.20.58.192",
"172.20.59.195",
"172.20.6.68",
"172.20.60.195",
"172.20.61.68",
"172.20.62.195",
"172.20.63.68",
"172.20.64.64",
"172.20.65.69",
"172.20.48.195",
"172.20.66.196",
"172.20.67.69",
"172.20.68.196",
"172.20.49.68",
"172.20.50.195",
"172.20.51.68",
"172.20.52.195",
"172.20.53.68",
"172.20.55.195",
"172.20.56.68",  # Add all 20 IPs here
]
USERNAME = "docker"  # Shared username
RDP_PORT = 3389  # Default RDP port


def connect_to_rdp(ip, username):
    try:
        print(f"Attempting to connect to RDP at {ip} with username: {username}")
        with socket.create_connection((ip, RDP_PORT), timeout=10) as conn:
            # Example RDP handshake packet; modify as needed
            conn.sendall(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
            response = conn.recv(1024)
            if response:
                print(f"Connection to {ip} successful with username: {username}")
            else:
                print(f"Failed to connect to {ip}. No response.")
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")


if __name__ == "__main__":
    for ip in POD_IPS:
        connect_to_rdp(ip, USERNAME)
