for ns in $(kubectl get namespaces -l team=ctf --no-headers | awk '{print $1}'); do
  echo "Applying Role & RoleBinding to namespace: $ns"
  
  cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: node-health-check-role
  namespace: $ns
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "delete"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "delete"]
  - apiGroups: [""]
    resources: ["persistentvolumeclaims"]
    verbs: ["get", "list", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: node-health-check-binding
  namespace: $ns
subjects:
  - kind: ServiceAccount
    name: node-health-check-sa
    namespace: kube-system
roleRef:
  kind: Role
  name: node-health-check-role
  apiGroup: rbac.authorization.k8s.io
EOF

done
