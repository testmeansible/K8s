#!/bin/bash
#----------------------------------------------------------------------------------------------------------------------------------------
#--[1.1]- Modules 
sudo tee /etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter
 
#--/etc/modules-load.d
#--overlay: pod network abstraction 
#--br_netfilter: bridge netfilter support - required for networking and policy
 
#--[1.2]- Force IPv4 and IPv6 traffic to pass through iptables. 
 
#-- Reason: Required for for most of CNI and Kubernetes networking policies to eable IPv4 and IPv6 traffic to be passed to iptables chains.
#--         Kubernetes requires that packets traversing a network bridge are processed for filtering and for port forwarding. 
#--         To achieve this, tunable parameters in the kernel bridge module are automatically set when the kubeadm package is installed and a 
#--         sysctl file is created at /etc/sysctl.d/99-kubernetes-cri.conf that contains the following lines: 
 
sudo tee /etc/sysctl.d/kubernetes.conf <<EOT
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOT
 
#--sysctl is used for modifying linux kernel variable.
#--sysctl -a command can be used to check all values.
sudo sysctl --system
 
#--[1.3]- Disable firewall 
# sudo ufw disable
 
#--[1.4]- Disable swap  
sudo swapoff -a  
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab  
sudo sed -i '/ swap / s/^/#/' /etc/fstab


#--[1.5]- Install  necessary 
sudo apt-get update  
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common gpg
 
############################################################################################################################################
#--[2]- Install containerd
############################################################################################################################################
#--[2.1]- Install containerd
sudo apt-get update
sudo apt-get install -y containerd

#--[2.2]- Configure containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

# Enable SystemdCgroup
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

#--[2.3]- Start and enable containerd service
sudo systemctl restart containerd
sudo systemctl enable containerd

############################################################################################################################################
#--[3]- Install Kubectl, Kubeadm and Kubelet
############################################################################################################################################
#--[3.1]- Add keys and repo 
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

#curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
#echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list


#--apt-cache policy kubelet | head -n 20 
#--[3.2]- Install 
sudo apt update 
sudo apt install -y kubelet kubeadm kubectl 
 
#--[3.3]- Stop automatic update 
sudo apt-mark hold kubelet kubeadm kubectl  
 
#-----------------------------------------------------------------------------------------------------------------------------------------

############################################################################################################################################
#--[4]- Validation
############################################################################################################################################
 
#--[4.1]- Check memory 
free -m  

#--[4.2]- Check ufw 
sudo ufw status 
