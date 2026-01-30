# import json
# import requests

# # Load user data from JSON
# with open("users-3.json", "r") as f:
#     users = json.load(f)

# # API endpoint
# url = "http://192.168.3.156:8000/user/create/"

# # Loop through users and send POST request
# for user in users:
#     response = requests.post(url, json=user)

#     # Print response summary
#     if response.status_code == 201:
#         print(f"✅ Created: {user['username']}")
#     else:
#         print(f"❌ Failed for {user['username']} | Status: {response.status_code} | Response: {response.text}")

import json
import requests
import time

# Load user data from JSON
with open("cyber-drill.json", "r") as f:
    users = json.load(f)

# API endpoint
url = "http://192.168.3.156:8000/user/create/"

# Loop through users and send POST request
for idx, user in enumerate(users, start=1):
    response = requests.post(url, json=user)

    # Print response summary
    if response.status_code == 201:
        print(f"✅ Created: {user['username']}")
    else:
        print(f"❌ Failed for {user['username']} | Status: {response.status_code} | Response: {response.text}")

    # Wait 12 seconds after each request (5/minute limit)
    if idx < len(users):
        time.sleep(15)
