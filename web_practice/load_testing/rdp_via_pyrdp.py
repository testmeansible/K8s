from pyrdp.rdp import RDPClient
from pyrdp.layers import RDPGfx

POD_IPS = [
    "172.20.13.68", "172.20.57.195", # Add your IPs here
]

USERNAME = "docker"
RDP_PORT = 3389

def connect_to_rdp(ip, username):
    try:
        print(f"Connecting to {ip}...")
        client = RDPClient(ip, RDP_PORT, username)
        client.start()  # Initiates the connection
        print(f"Connection to {ip} successful")
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")

if __name__ == "__main__":
    for ip in POD_IPS:
        connect_to_rdp(ip, USERNAME)
