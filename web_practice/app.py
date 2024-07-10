from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config
import os

app = Flask(__name__)

# Load Kubernetes configuration from a specific kubeconfig file
kubeconfig_path = os.path.join(os.path.expanduser("~"), ".kube", "config")  # Update this path if necessary
config.load_kube_config(config_file=kubeconfig_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_pod', methods=['POST'])
def create_pod():
    pod_name = request.form['pod_name']
    namespace = request.form['namespace']

    # Define the pod specification
    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(
            containers=[client.V1Container(
                name="nginx",
                image="nginx:latest",
                ports=[client.V1ContainerPort(container_port=80)]
            )]
        )
    )

    # Create the pod in the specified namespace
    api_instance = client.CoreV1Api()
    api_instance.create_namespaced_pod(namespace=namespace, body=pod)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
