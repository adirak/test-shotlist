#!/usr/bin/env bash
command -v kind >/dev/null || { curl -sLo /tmp/kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x /tmp/kind && sudo mv /tmp/kind /usr/local/bin/kind; }
docker start shotlist-control-plane 2>/dev/null || true
sleep 5
kind export kubeconfig --name shotlist 2>/dev/null || true
