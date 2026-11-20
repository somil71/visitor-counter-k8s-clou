# Deploy a Visitor Counter Web App (Flask + Redis) on Docker and Kubernetes

> **Cloud Computing Final Project Submission**  
> **Technologies:** Python Flask, Redis, Docker, Kubernetes, HPA, Hybrid Cloud Failover, Cloud Cost Optimization.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Quick Start Guide](#quick-start-guide)
  - [Task a: Containerization with Docker](#task-a-containerize-the-application)
  - [Task b: Deployment on Kubernetes](#task-b-deploy-the-application-on-kubernetes)
  - [Task c: HPA Autoscaling](#task-c-implement-hpa-autoscaling)
  - [Task d: Hybrid Cloud with Failover](#task-d-implement-hybrid-cloud-with-failover)
  - [Task e: Cost Optimization](#task-e-cost-optimization-techniques)
- [Screenshots Checklist](#screenshots-checklist)

---

## 🚀 Overview
This repository contains the complete implementation of a production-ready, distributed Visitor Counter microservice architecture designed to meet all 5 requirements of the Cloud Computing project.

---

## 📁 Project Structure
```text
E:\CLOUD_PROJECT\
│
├── app\                         # Flask application & Docker assets
│   ├── app.py                   # Main Flask app (visitor counter, health check, CPU load generator)
│   ├── requirements.txt         # Dependencies (Flask, Redis, Gunicorn)
│   ├── Dockerfile               # Baseline Docker image (Task a)
│   ├── Dockerfile.optimized     # Multi-stage slim image (Task e Cost Optimization)
│   ├── docker-compose.yml       # Local container orchestration
│   └── templates\
│       └── index.html           # Modern responsive dashboard UI
│
├── k8s\                         # Declarative Kubernetes Manifests
│   ├── configmap.yaml           # Environment configurations
│   ├── redis-deployment.yaml    # Redis Deployment with health probes
│   ├── redis-service.yaml       # Redis internal ClusterIP service
│   ├── flask-deployment.yaml    # Flask Deployment with resource requests & probes
│   ├── flask-service.yaml       # Flask NodePort service (port 30080)
│   └── hpa.yaml                 # Horizontal Pod Autoscaler manifest
│
├── failover\                    # Task (d) Hybrid Cloud Failover Assets
│   ├── cloud_standby.py         # Standby Public Cloud DR microservice (port 5001)
│   ├── nginx-failover.conf      # NGINX reverse-proxy configuration with health checks
│   └── simulate_failover.py     # Automated failover verification monitor
│
├── cost_optimization\           # Task (e) Cost Optimization Documentation
│   └── cost_analysis_report.md  # Detailed before-and-after metrics, formulas & dollar savings
│
├── scripts\                     # One-click execution scripts
│   ├── 1_docker_test.ps1        # Build and run Docker containers
│   ├── 2_k8s_deploy.ps1         # Apply Kubernetes manifests
│   ├── 3_failover_test.ps1      # Test automated failover
│   ├── 4_benchmark_costs.ps1    # Display cost optimization metrics
│   └── load_test.py             # Multi-threaded load tester for HPA
│
└── docs\                        # Submission Documentation
    ├── Project_Report.md        # Comprehensive submission report
    └── SCREENSHOTS_GUIDE.md     # Exact checklist of screenshots to submit
```

---

## ⚡ Quick Start Guide

### Prerequisites
- Docker Desktop
- Minikube or Kubernetes enabled
- Kubectl CLI
- Python 3.10+

---

### Task (a): Containerize the Application
Run locally with Docker Compose:
```powershell
cd E:\CLOUD_PROJECT\app
docker compose up -d --build
```
Access the app in your browser at: `http://localhost:5000`  
Health check endpoint: `http://localhost:5000/health`

---

### Task (b): Deploy the Application on Kubernetes
Deploy to your Kubernetes cluster:
```powershell
cd E:\CLOUD_PROJECT\scripts
.\2_k8s_deploy.ps1
```
Or manually:
```powershell
cd E:\CLOUD_PROJECT\k8s
kubectl apply -f configmap.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```
Access via NodePort: `http://localhost:30080` (or run `minikube service flask-service`).

---

### Task (c): Implement HPA Autoscaling
1. Ensure the metrics server is enabled:
```powershell
minikube addons enable metrics-server
```
2. Verify HPA status:
```powershell
kubectl get hpa flask-hpa -w
```
3. Run the concurrent load generator:
```powershell
python E:\CLOUD_PROJECT\scripts\load_test.py 15 60
```
Watch the pod count scale out from **2 replicas up to 6 replicas** as CPU utilization exceeds the 50% threshold.

---

### Task (d): Implement Hybrid Cloud with Failover
Run the automated failover test:
```powershell
cd E:\CLOUD_PROJECT\scripts
.\3_failover_test.ps1
```
While running, simulate primary cluster failure in another terminal:
```powershell
kubectl scale deployment flask-deployment --replicas=0
```
Observe the monitor automatically routing traffic to the Secondary Cloud DR Standby without 502 errors!  
Restore primary:
```powershell
kubectl scale deployment flask-deployment --replicas=2
```

---

### Task (e): Cost Optimization Techniques
View the complete cost report in: [`docs/Project_Report.md`](docs/Project_Report.md) or [`cost_optimization/cost_analysis_report.md`](cost_optimization/cost_analysis_report.md).

| Technique | Baseline Metric | Optimized Metric | Measured Reduction |
| :--- | :--- | :--- | :--- |
| **1. Multi-Stage Slim Build** | 1,020 MB | 126 MB | **87.6% Image Size Reduction** |
| **2. Pod Resource Right-Sizing** | 500m CPU / 512Mi RAM | 50m CPU / 64Mi RAM | **600% Pod Density Increase** |
| **3. Dynamic Elastic HPA** | 4,320 pod-hrs/mo | 2,040 pod-hrs/mo | **52.8% Compute Hour Reduction** |
