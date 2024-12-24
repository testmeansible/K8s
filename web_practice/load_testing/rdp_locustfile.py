from locust import User, task, between
import pyrdpclient  # Example RDP client library
import time
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
"172.20.56.68"]
RDP_PORT = 3389
USERNAME = "docker"
PASSWORD = ""

class RDPUser(User):
    wait_time = between(1, 5)

    @task
    def connect_rdp(self):
        for ip in POD_IPS:
            try:
                client = pyrdpclient.RDPClient(ip, RDP_PORT, USERNAME, PASSWORD)
                start_time = time.time()
                client.connect()
                end_time = time.time()
                print(f"Connected to {ip}. Init time: {end_time - start_time:.2f}s")
                client.disconnect()
            except Exception as e:
                print(f"Error connecting to {ip}: {e}")
