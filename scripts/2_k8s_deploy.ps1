# PowerShell Script: Task (b) & (c) Kubernetes Deployment & HPA Setup
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Step 2: Deploying to Kubernetes Cluster                 " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location "E:\CLOUD_PROJECT\k8s"

Write-Host "`n[1/5] Applying ConfigMap..." -ForegroundColor Yellow
kubectl apply -f configmap.yaml

Write-Host "`n[2/5] Deploying Redis (Deployment & Service)..." -ForegroundColor Yellow
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml

Write-Host "`n[3/5] Deploying Flask Application..." -ForegroundColor Yellow
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml

Write-Host "`n[4/5] Applying Horizontal Pod Autoscaler (HPA)..." -ForegroundColor Yellow
kubectl apply -f hpa.yaml

Write-Host "`n[5/5] Checking Kubernetes Cluster Resources..." -ForegroundColor Green
kubectl get configmaps
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl get hpa

Write-Host "`n[+] Verification:" -ForegroundColor Green
Write-Host "    NodePort URL: http://localhost:30080"
Write-Host "    (If using minikube: run 'minikube service flask-service')"
Write-Host "==========================================================" -ForegroundColor Cyan
