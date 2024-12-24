from kubernetes import client, config


kubeconfig_path = './production.yaml'

# Load the Kubernetes config (from ~/.kube/config or in-cluster config)
config.load_kube_config(config_file=kubeconfig_path)  # Use config.load_incluster_config() if running inside the cluster

# Create a client for the Kubernetes CustomObjects API
api_instance = client.CustomObjectsApi()

# Define the group, version, and plural for Calico IP pools
group = "projectcalico.org"
version = "v3"
plural = "ippools"

# Define the new IP pool object
ip_pool = {
    "apiVersion": "projectcalico.org/v3",
    "kind": "IPPool",
    "metadata": {
        "name": "new-custom-ip-pool-team-a"  # Name of the IP pool
    },
    "spec": {
        "cidr": "172.16.88.0/24",  # Define the CIDR for the IP pool
        "ipipMode": "Always",  # Enable IP-in-IP mode for cross-node pod communication
        "natOutgoing": True,  # Enable NAT for outgoing traffic
        "blockSize": 26  # Define block size for allocation
    }
}

try:
    # Create the new IP pool in the cluster
    api_response = api_instance.create_cluster_custom_object(
        group=group,
        version=version,
        plural=plural,
        body=ip_pool
    )
    print("IP Pool created successfully.")
    print(api_response)
    
except client.exceptions.ApiException as e:
    print(f"Exception when creating IP pool: {e}")

