head -1 /workspaces/.codespaces/.persistedshare/creation.log#!/usr/bin/env bash
set -euo pipefail
if ! command -v kubectl >/dev/null; then
  curl -sLo /tmp/kubectl "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  chmod +x /tmp/kubectl && sudo mv /tmp/kubectl /usr/local/bin/kubectl
fi
if ! command -v kind >/dev/null; then
  curl -sLo /tmp/kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
  chmod +x /tmp/kind && sudo mv /tmp/kind /usr/local/bin/kind
fi
if ! kind get clusters 2>/dev/null | grep -qx shotlist; then
cat <<'KIND' | kind create cluster --name shotlist --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - { containerPort: 80, hostPort: 80 }
      - { containerPort: 443, hostPort: 443 }
KIND
fi
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
kubectl wait -n ingress-nginx --for=condition=ready pod -l app.kubernetes.io/component=controller --timeout=180s
echo "cluster ready -> bash scripts/deploy.sh"
