#!/bin/bash

SA_NAME=cyberrange-app
NAMESPACE=ctf-control
CLUSTER_NAME=$(kubectl config view --minify -o jsonpath='{.clusters[0].name}')
CLUSTER_SERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
SECRET_NAME=$(kubectl get sa $SA_NAME -n $NAMESPACE -o jsonpath='{.secrets[0].name}')
CA_CERT=$(kubectl get secret $SECRET_NAME -n $NAMESPACE -o jsonpath='{.data.ca\.crt}' | base64 --decode)
TOKEN=$(kubectl get secret $SECRET_NAME -n $NAMESPACE -o jsonpath='{.data.token}' | base64 --decode)

cat <<EOF > cyberrange-kubeconfig.yaml
apiVersion: v1
kind: Config
clusters:
- name: $CLUSTER_NAME
  cluster:
    server: $CLUSTER_SERVER
    certificate-authority-data: $(echo "$CA_CERT" | base64 | tr -d '\n')
contexts:
- name: cyberrange
  context:
    cluster: $CLUSTER_NAME
    user: cyberrange
    namespace: default
current-context: cyberrange
users:
- name: cyberrange
  user:
    token: $TOKEN
EOF

echo "[+] cyberrange-kubeconfig.yaml generated successfully!"
