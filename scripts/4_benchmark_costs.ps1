# PowerShell Script: Task (e) Cost Optimization Metrics Inspector
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Step 4: Cost Optimization Benchmark & Measurements       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Write-Host "`n--- [Technique 1: Image Size Comparison] ---" -ForegroundColor Yellow
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Select-String "visitor-app"

Write-Host "`n--- [Technique 2: Kubernetes Pod Resource Limits] ---" -ForegroundColor Yellow
kubectl describe deployment flask-deployment | Select-String -Pattern "Limits|Requests|cpu|memory" -Context 0,2

Write-Host "`n--- [Technique 3: Horizontal Pod Autoscaler Active Stats] ---" -ForegroundColor Yellow
kubectl get hpa flask-hpa

Write-Host "`n[+] Full report available at: E:\CLOUD_PROJECT\cost_optimization\cost_analysis_report.md" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
