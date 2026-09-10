# ShotList

Photography shoot management — React + FastAPI + Postgres.
Week 6 target: run the whole stack on local Kubernetes (kind) behind an Ingress.

## 1. Codespace

Open in GitHub Codespaces (4-core recommended). First time only:

```bash
bash .devcontainer/setup-cluster.sh
```

## 2. docker compose (sanity check first)

```bash
docker compose up --build
```

Open the forwarded port **8080** → the app. **8000/docs** → the API.

## 3. Kubernetes

```bash
bash scripts/deploy.sh
kubectl get pods -n shotlist -w
```

Open the forwarded port **80** → the app through Ingress. `/api/docs` → the API.

## Debug cheatsheet

```bash
kubectl get pods -n shotlist
kubectl describe pod -n shotlist <pod>          # Events + Last State
kubectl logs -n shotlist <pod> --previous       # crashed container
kubectl get endpoints -n shotlist               # empty = label / readiness
kubectl port-forward -n shotlist svc/api 9000:8000
kubectl describe ingress -n shotlist shotlist
```

## Layout

```
backend/    FastAPI + SQLAlchemy 2.0 + Alembic
frontend/   Vite + React, served by nginx
k8s/        Namespace, Secret/ConfigMap, Deployments, Services, Ingress
scripts/    deploy.sh
```
