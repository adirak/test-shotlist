#!/usr/bin/env bash
# build images -> load into kind -> apply manifests
set -euo pipefail
cd "$(dirname "$0")/.."

docker build -t shotlist-api:dev ./backend
docker build -t shotlist-web:dev ./frontend
kind load docker-image shotlist-api:dev shotlist-web:dev --name shotlist

kubectl apply -f k8s/
kubectl rollout restart deployment/api deployment/web -n shotlist 2>/dev/null || true
kubectl get pods -n shotlist
