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

try:
    # List all IP pools in the cluster
    ip_pools = api_instance.list_cluster_custom_object(group=group, version=version, plural=plural)
    
    # Loop through and print each IP pool's name and CIDR
    for pool in ip_pools['items']:
        print(f"Name: {pool['metadata']['name']}, CIDR: {pool['spec']['cidr']}")
        
except client.exceptions.ApiException as e:
    print(f"Exception when listing IP pools: {e}")

