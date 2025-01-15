from locust import TaskSet, task, HttpUser, between
import subprocess
import time

# List of pod IPs or hostnames
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
"172.20.56.68"
  # Add all pod IPs
    # Continue up to 20 pods
]
RDP_PORT = 3389  # Default RDP port

class RDPTaskSet(TaskSet):
    def on_start(self):
        # Assign a unique pod IP to each user
        self.pod_ip = POD_IPS[self.user.user_id % len(POD_IPS)]
        print(f"User assigned to pod: {self.pod_ip}")

    @task
    def connect_to_rdp(self):
        try:
            with socket.create_connection((self.pod_ip, RDP_PORT), timeout=10) as s:
                s.send(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")  # Basic RDP initiation
                response = s.recv(1024)
                if response:
                    print(f"Successfully connected to {self.pod_ip}")
                else:
                    print(f"Failed to receive response from {self.pod_ip}")
        except Exception as e:
            print(f"Failed to connect to {self.pod_ip}: {e}")

class RDPUser(HttpUser):
    tasks = [RDPTaskSet]
    wait_time = between(1, 5)  # Adjust as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = self.environment.runner.user_count