for ns in $(kubectl get ns -l team=ctf --no-headers | awk '{print $1}'); do
  echo "Applying Role & RoleBinding to namespace: $ns"
  
  cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: blueteamapp-manager
  namespace: $ns
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["create", "delete", "get", "list", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods", "configmaps", "secrets"]
    verbs: ["create", "delete", "get", "list", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: blueteamapp-binding
  namespace: $ns
subjects:
  - kind: ServiceAccount
    name: blueteamapp-sa
    namespace: kube-system
roleRef:
  kind: Role
  name: blueteamapp-manager
  apiGroup: rbac.authorization.k8s.io
EOF

done
