# PowerShell Script: Task (a) Containerization & Local Verification
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Step 1: Building Docker Images (Baseline & Optimized)   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location "E:\CLOUD_PROJECT\app"

Write-Host "`n[1/4] Building Baseline Image (python:3.11)..." -ForegroundColor Yellow
docker build -t visitor-app:baseline -f Dockerfile .

Write-Host "`n[2/4] Building Optimized Image (python:3.11-slim Multi-stage)..." -ForegroundColor Yellow
docker build -t visitor-app:latest -t visitor-app:optimized -f Dockerfile.optimized .

Write-Host "`n[3/4] Comparing Image Sizes (Task 'e' Cost Metric 1)..." -ForegroundColor Green
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | Select-String "visitor-app"

Write-Host "`n[4/4] Starting Containers with Docker Compose..." -ForegroundColor Yellow
docker compose up -d

Write-Host "`n[*] Container status:" -ForegroundColor Cyan
docker compose ps

Write-Host "`n[+] Verification:" -ForegroundColor Green
Write-Host "    Open browser at: http://localhost:5000"
Write-Host "    Test API at:     http://localhost:5000/api/count"
Write-Host "    Health check:    http://localhost:5000/health"
Write-Host "==========================================================" -ForegroundColor Cyan
