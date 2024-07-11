from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config
import os

app = Flask(__name__)

# Load Kubernetes configuration from a specific kubeconfig file
kubeconfig_path = os.path.join(os.path.expanduser("~"), ".kube", "config")  # Update this path if necessary
config.load_kube_config(config_file=kubeconfig_path)

# Configure Kubernetes client
# config.load_kube_config()  # Assuming kubectl config is set up
v1 = client.AppsV1Api()


# Predefined pod configurations (modify as needed)
pod_definitions = {
    "nginx": {
        "image": "nginx:latest",
        "name": "nginx-pod",
        "resources": {"requests": {"cpu": "100m", "memory": "1Gi"}},
    },
    "busybox": {
        "image": "busybox:latest",
        "name": "busybox-pod",
        "command": ["sleep", "3600"],  # Run for 1 hour
    },
}


@app.route("/")
def index():
    return render_template("index.html", pod_names=pod_definitions.keys())


@app.route("/deploy", methods=["POST"])
def deploy_pod():
    pod_name = request.form.get("pod_name")
    if not pod_name or pod_name not in pod_definitions:
        return "Invalid pod selection!", 400

    pod_data = pod_definitions[pod_name]
    pod_manifest = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_data["name"]),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name=pod_name,
                    image=pod_data["image"],
                    command=pod_data.get("command"),
                    resources=pod_data.get("resources"),
                )
            ]
        ),
    )

    try:
        v1.create_namespaced_pod(body=pod_manifest, namespace="default")
        return f"Pod '{pod_name}' deployed successfully!"
    except client.ApiException as e:
        return f"Deployment failed: {e.body}", 500


if __name__ == "__main__":
    app.run(debug=True)
