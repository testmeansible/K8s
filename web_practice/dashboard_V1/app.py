from flask import Flask, render_template, request, redirect, url_for
from kubernetes import client, config

app = Flask(__name__)

# Load kube config
config.load_kube_config()
v1 = client.CoreV1Api()

@app.route('/')
def index():
    # Get namespaces and pods
    namespaces = {ns.metadata.name: [] for ns in v1.list_namespace().items}
    for namespace in namespaces.keys():
        pods = v1.list_namespaced_pod(namespace)
        namespaces[namespace] = [{
            'name': pod.metadata.name,
            'namespace': pod.metadata.namespace,
            'status': pod.status.phase,
            'pod_ip': pod.status.pod_ip,
            'node_name': pod.spec.node_name
        } for pod in pods.items]

    # Node and Namespace summary data (placeholder example)
    node_summary = {}
    namespace_summary = {}

    return render_template(
        'index.html',
        namespaces=namespaces,
        node_summary=node_summary,
        namespace_summary=namespace_summary
    )

@app.route('/create_pod', methods=['GET', 'POST'])
def create_pod():
    if request.method == 'POST':
        namespace = request.form['namespace']
        pod_name = request.form['pod_name']
        container_image = request.form['container_image']

        # Create pod
        pod = client.V1Pod(
            metadata=client.V1ObjectMeta(name=pod_name),
            spec=client.V1PodSpec(
                containers=[client.V1Container(name=pod_name, image=container_image)]
            )
        )
        v1.create_namespaced_pod(namespace=namespace, body=pod)

        return redirect(url_for('index'))

    namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
    return render_template('create_pod.html', namespaces=namespaces)

@app.route('/delete_pod', methods=['GET', 'POST'])
def delete_pod():
    if request.method == 'POST':
        namespace = request.form['namespace']
        pod_name = request.form['pod_name']

        # Delete pod
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)

        return redirect(url_for('index'))

    namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
    return render_template('delete_pod.html', namespaces=namespaces)

if __name__ == '__main__':
    app.run(debug=True)
