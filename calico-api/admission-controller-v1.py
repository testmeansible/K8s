import os
import subprocess
import json
from flask import Flask, request, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = Flask(__name__)

def init_k8s_client():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()
    return client.CoreV1Api()

k8s_client = init_k8s_client()

# Fetch the master pool based on label and subnet size
def get_master_pool(label_selector, cidr):
    try:
        command = ["calicoctl", "get", "ippool", "-o", "json", "-l", label_selector]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        ip_pools = json.loads(result.stdout.decode('utf-8'))['items']
        
        for pool in ip_pools:
            if pool['spec']['cidr'] == cidr:
                return pool
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error fetching IP pools: {e.stderr.decode('utf-8')}")
        return None

# Split the master pool into smaller subnets using calicoctl
def split_master_pool(cidr, new_subnet_size):
    try:
        cmd = ["calicoctl", "ipam", "split", cidr, new_subnet_size]
        output = subprocess.check_output(cmd)
        subnets = output.decode('utf-8').strip().split("\n")
        return subnets
    except subprocess.CalledProcessError as e:
        print(f"Failed to split IP pool: {e.output.decode('utf-8')}")
        return []

# Select the first available subnet
def select_available_subnet(subnets):
    if subnets:
        return subnets[0]
    return None

# Mark the IP pool as available again when a namespace is deleted
def mark_pool_as_available(namespace):
    try:
        # Fetch the pool associated with the namespace
        # Assuming the pool is stored in an annotation
        ns = k8s_client.read_namespace(namespace)
        ip_pool_annotation = ns.metadata.annotations.get("ip-pool")
        
        if ip_pool_annotation:
            patch = [{"op": "remove", "path": "/metadata/annotations/ip-pool"}]
            k8s_client.patch_namespace(name=namespace, body=patch)
            print(f"IP pool {ip_pool_annotation} marked as available.")
    except ApiException as e:
        print(f"Could not fetch IP pool for namespace: {e.reason}")

@app.route('/mutate', methods=['POST'])
def handle_admission_review():
    admission_review_req = request.get_json()
    admission_response = {
        "uid": admission_review_req['request']['uid'],
        "allowed": True
    }

    if admission_review_req['request']['kind']['kind'] == "Namespace":
        operation = admission_review_req['request']['operation']

        if operation == "CREATE":
            # Fetch the master IP pool with label "location" and /16 subnet
            label_selector = "location=my-location"
            master_pool = get_master_pool(label_selector, "/16")
            if not master_pool:
                return jsonify({
                    "response": {
                        "uid": admission_response['uid'],
                        "allowed": False,
                        "status": {
                            "message": "No matching IP pool found."
                        }
                    }
                })

            # Split the master pool into /26 subnets
            subnets = split_master_pool(master_pool['spec']['cidr'], "/26")
            if not subnets:
                return jsonify({
                    "response": {
                        "uid": admission_response['uid'],
                        "allowed": False,
                        "status": {
                            "message": "Could not split master pool."
                        }
                    }
                })

            # Select an available subnet
            available_pool = select_available_subnet(subnets)
            if not available_pool:
                return jsonify({
                    "response": {
                        "uid": admission_response['uid'],
                        "allowed": False,
                        "status": {
                            "message": "No available subnets found."
                        }
                    }
                })

            # Patch the namespace with the selected IP pool
            patch = [{"op": "add", "path": "/metadata/annotations/ip-pool", "value": available_pool}]
            admission_response['patch'] = json.dumps(patch)
            admission_response['patchType'] = "JSONPatch"

        elif operation == "DELETE":
            # Handle namespace deletion - mark IP pool as available again
            namespace = admission_review_req['request']['name']
            mark_pool_as_available(namespace)

    return jsonify({
        "response": admission_response
    })

if __name__ == '__main__':
    cert_file = "/tls/tls.crt"
    key_file = "/tls/tls.key"
    app.run(host='0.0.0.0', port=8443, ssl_context=(cert_file, key_file))
