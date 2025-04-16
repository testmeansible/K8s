## Expose Dashboard via NodePort
### If you want permanent external access, change the service type to NodePort:

kubectl patch svc kubernetes-dashboard-kong-proxy -n kubernetes-dashboard \
  -p '{"spec": {"type": "NodePort"}}'

### Then, find the NodePort assigned:

kubectl get svc kubernetes-dashboard-kong-proxy -n kubernetes-dashboard

### Access it via:

https://<NODE_IP>:<NODEPORT>
