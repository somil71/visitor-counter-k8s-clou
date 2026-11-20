# PowerShell Script: Task (d) Hybrid Cloud Failover Verification
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Step 3: Hybrid Cloud with Failover Demonstration        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location "E:\CLOUD_PROJECT\failover"

Write-Host "`n[1/3] Starting Standby Cloud Disaster Recovery Server on port 5001..." -ForegroundColor Yellow
$proc = Start-Process python -ArgumentList "cloud_standby.py" -PassThru
Start-Sleep -Seconds 2

Write-Host "[+] Cloud Standby running with Process ID: $($proc.Id)" -ForegroundColor Green

Write-Host "`n[2/3] Running automated failover test monitor..." -ForegroundColor Yellow
Write-Host "TIP: While this test is running, simulate a primary failure by running:" -ForegroundColor Magenta
Write-Host "     kubectl scale deployment flask-deployment --replicas=0" -ForegroundColor Magenta
Write-Host "Then restore primary by running:" -ForegroundColor Magenta
Write-Host "     kubectl scale deployment flask-deployment --replicas=2" -ForegroundColor Magenta

python simulate_failover.py 20

Write-Host "`n[3/3] Stopping Standby Server process..." -ForegroundColor Yellow
Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue

Write-Host "[+] Failover test concluded." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
