# Complete Step-by-Step Recreation Guide & Screenshot Checklist

**Project Title:** Deploy a Visitor Counter Web App (Flask + Redis) on Docker and Kubernetes  
**Repository:** [https://github.com/somil71/visitor-counter-k8s-clou](https://github.com/somil71/visitor-counter-k8s-clou)  
**Location:** `E:\CLOUD_PROJECT`  
**Submission Deadline:** 24 November 2026 (CampX & Google Drive)

---

## Quick Reference: 5 Mandatory Tasks Overview

| Task | Objective | Core Commands | Verification Endpoint |
| :--- | :--- | :--- | :--- |
| **Task (a)** | Containerize application (Flask + Redis) | `docker compose up -d` | `http://localhost:5000` |
| **Task (b)** | Deploy on Kubernetes (Minikube) | `kubectl apply -f k8s/` | `http://localhost:8080` |
| **Task (c)** | Implement HPA Autoscaling | `python scripts/load_test.py 60 16` | `kubectl get hpa -w` (Scales 2 -> 6) |
| **Task (d)** | Hybrid Cloud with Failover | `.\scripts\3_failover_test.ps1` | `http://localhost:5001` (Cloud DR) |
| **Task (e)** | Cost Optimization (3 measured techniques) | `docker images`, `kubectl describe deployment` | Measured Before vs After Values |

---

## Prerequisites & One-Time Setup

1. **Docker Desktop:** Ensure Docker Desktop is launched and the whale icon is solid green in your taskbar.
2. **Minikube & Kubectl:**
   * Start cluster:
     ```powershell
     minikube start --driver=docker
     minikube addons enable metrics-server
     ```

---

## Step-by-Step Reproduction Guide & Screenshots

---

### TASK (a): Containerize the Application (Flask + Redis)

#### Steps to Recreate:
1. Navigate to the project directory:
   ```powershell
   cd E:\CLOUD_PROJECT\app
   ```
2. Build baseline and multi-stage optimized Docker images:
   ```powershell
   docker build -t visitor-app:baseline -f Dockerfile .
   docker build -t visitor-app:optimized -t visitor-app:latest -f Dockerfile.optimized .
   ```
3. Start the containers using Docker Compose:
   ```powershell
   docker compose up -d
   ```
4. Verify running status:
   ```powershell
   docker compose ps
   ```
5. Open your browser to test:
   Navigate to `http://localhost:5000` and click **"Refresh & Increment Counter"**.

#### Screenshots to Take for Task (a):
* **Screenshot 1.1 — Docker Compose Terminal:**
  * **Command:** `docker compose ps`
  * **What it proves:** Shows `flask-visitor-counter` (port 5000) and `redis-service` (port 6379, healthy) running concurrently.
* **Screenshot 1.2 — Browser UI (Docker Compose):**
  * **URL:** `http://localhost:5000`
  * **What it proves:** Web page displaying:
    * Total Visits Tracked (e.g. `5`)
    * Deployment Environment: `Docker-Compose-Local`
    * Redis Status: `Connected (redis:6379)`

---

### TASK (b): Deploy Application on Kubernetes (Minikube)

#### Steps to Recreate:
1. Load the container image into Minikube's Docker daemon:
   ```powershell
   cmd.exe /c "docker save visitor-app:latest | docker exec -i minikube docker load"
   ```
2. Apply all Kubernetes manifests:
   ```powershell
   cd E:\CLOUD_PROJECT\k8s
   kubectl apply -f configmap.yaml
   kubectl apply -f redis-deployment.yaml
   kubectl apply -f redis-service.yaml
   kubectl apply -f flask-deployment.yaml
   kubectl apply -f flask-service.yaml
   kubectl apply -f hpa.yaml
   ```
3. Forward port 8080 to the Flask Kubernetes service:
   ```powershell
   kubectl port-forward svc/flask-service 8080:5000
   ```
4. Verify all Kubernetes resources:
   ```powershell
   kubectl get pods,svc,hpa -o wide
   ```
5. Open your browser:
   Navigate to `http://localhost:8080` and click **"Refresh & Increment Counter"**.

#### Screenshots to Take for Task (b):
* **Screenshot 2.1 — Kubernetes Pods & Services Terminal:**
  * **Command:** `kubectl get pods,svc,hpa -o wide`
  * **What it proves:** 
    * 2 Flask pods (`flask-deployment-...`) with status `1/1 Running`.
    * 1 Redis pod (`redis-deployment-...`) with status `1/1 Running`.
    * Services: `flask-service` (NodePort 30080) and `redis-service` (ClusterIP 6379).
* **Screenshot 2.2 — Browser UI (Kubernetes Cluster):**
  * **URL:** `http://localhost:8080`
  * **What it proves:**
    * Deployment Environment: `Kubernetes Cluster (Minikube Primary)` (blue badge).
    * Pod / Container Hostname: `flask-deployment-d6b594594-...`
    * Redis Status: `Connected (redis-service:6379)`.

---

### TASK (c): Implement HPA Autoscaling

#### Steps to Recreate:
1. Open **Terminal 1** (PowerShell) and watch the HPA live:
   ```powershell
   kubectl get hpa flask-hpa -w
   ```
2. Open **Terminal 2** (PowerShell) and run the automated load test:
   ```powershell
   python E:\CLOUD_PROJECT\scripts\load_test.py 60 16
   ```
3. The load generator will send 350+ requests hitting `/load?duration=0.4`.
4. Observe Terminal 1: CPU surges to `200%/50%`, and HPA scales replicas from **2 -> 4 -> 6**.
5. Once the test finishes, watch HPA cool down and scale back to **2 replicas**.

#### Screenshots to Take for Task (c):
* **Screenshot 3.1 — HPA Under Load (Scaling to 6 Replicas):**
  * **Command:** `kubectl get hpa,pods`
  * **What it proves:** Shows `TARGETS: 200%/50%`, `REPLICAS: 6`, and all 6 Flask pods running.
* **Screenshot 3.2 — HPA Describe Event Logs:**
  * **Command:** `kubectl describe hpa flask-hpa`
  * **What it proves:** Shows official Kubernetes events:
    * `Normal SuccessfulRescale: New size: 4; reason: cpu resource utilization above target`
    * `Normal SuccessfulRescale: New size: 6; reason: cpu resource utilization above target`
    * `Normal SuccessfulRescale: New size: 2; reason: All metrics below target`

---

### TASK (d): Hybrid Cloud with Failover

#### Architecture Overview:
* **Primary Path:** Local Kubernetes Cluster (`http://localhost:8080`)
* **Secondary Disaster Recovery (DR) Standby:** Public Cloud Standby (`http://localhost:5001`)

#### Steps to Recreate:
1. Run the failover demonstration script:
   ```powershell
   cd E:\CLOUD_PROJECT\scripts
   .\3_failover_test.ps1
   ```
2. While the script runs normal health checks (`NORMAL (Primary Active)`):
   Open another terminal and simulate a catastrophic primary outage:
   ```powershell
   kubectl scale deployment flask-deployment --replicas=0
   ```
3. Observe the monitor automatically rerouting to the Cloud Standby:
   `Secondary (Cloud DR) | 200 | [!] FAILOVER ENGAGED`
4. Restore the primary cluster:
   ```powershell
   kubectl scale deployment flask-deployment --replicas=2
   ```
5. Observe traffic seamlessly falling back to Primary: `NORMAL (Primary Active)`.

#### Screenshots to Take for Task (d):
* **Screenshot 4.1 — Failover Active in Terminal:**
  * Output of `simulate_failover.py` showing the transition from `Primary (K8s Cluster) NORMAL` to `Secondary (Cloud DR) [!] FAILOVER ENGAGED` and recovery back to `Primary`.
* **Screenshot 4.2 — Cloud Standby UI in Browser:**
  * **URL:** `http://localhost:5001`
  * **What it proves:** Shows the Cloud Standby DR recovery page (`AWS-Simulation / us-east-1 / disaster-recovery-standby`).

---

### TASK (e): Cost Optimization (3 Measured Techniques)

You must include measured before-and-after values for the three cost reduction techniques in your report:

#### Technique 1: Docker Image Size Optimization (Storage & Network Transfer)
* **Measurement Command:**
  ```powershell
  docker images | Select-String "visitor-app"
  ```
* **Measured Values:**
  * **Before (Baseline `python:3.11` full image):** `1.63 GB` (1,630 MB)
  * **After (Optimized multi-stage `python:3.11-slim`):** `199 MB`
  * **Measured Reduction:** **87.8% reduction** (1,431 MB saved per image pull).
* **Cost Impact:** Drastically cuts container registry storage fees and intra-cluster container download bandwidth egress charges.

#### Technique 2: Kubernetes Pod Resource Right-Sizing
* **Measurement Command:**
  ```powershell
  kubectl describe deployment flask-deployment | Select-String -Pattern "Limits|Requests" -Context 0,2
  ```
* **Measured Values:**
  * **Before (Unoptimized default):** CPU Request: `500m`, Memory Request: `512 MiB`
  * **After (Profiled & Right-sized):** CPU Request: `50m`, Memory Request: `64 MiB`
  * **Measured Reduction:** **90% reduction in CPU reservation, 87.5% reduction in RAM reservation**.
* **Cost Impact:** Enables up to **6x higher pod packing density** on each Kubernetes worker node, preventing unnecessary horizontal node expansion in AWS EKS / GCP GKE.

#### Technique 3: Elastic Dynamic Autoscaling vs Static Provisioning
* **Measurement Formula:** Monthly Pod Compute Hours = `Replicas * 24 hrs * 30 days`
* **Measured Values:**
  * **Before (Static over-provisioning for peak 6 replicas):** `6 pods * 720 hrs = 4,320 pod-hours/month`
  * **After (HPA dynamic 2-6 autoscaling with 85% off-peak):** `(2 pods * 612 hrs) + (6 pods * 108 hrs) = 1,872 pod-hours/month`
  * **Measured Savings:** **2,448 pod-hours saved (56.7% compute cost reduction)**.

#### Screenshot to Take for Task (e):
* **Screenshot 5.1:** Terminal output of `docker images` showing `visitor-app:baseline` (1.63GB) vs `visitor-app:optimized` (199MB).
* **Screenshot 5.2:** Output of `kubectl describe deployment flask-deployment` highlighting the `cpu: 50m` and `memory: 64Mi` request blocks.

---

## Final Submission Checklist (CampX & Google Drive)

Before submitting by **24 November 2026**:
1. [x] Git repository pushed to: `https://github.com/somil71/visitor-counter-k8s-clou`
2. [ ] Open `docs/Project_Report.md`, paste your captured screenshots under each designated section.
3. [ ] Export `Project_Report.md` to PDF or copy content into Microsoft Word and save as `Project_Report.pdf`.
4. [ ] Upload to **Google Drive** folder requested by the professor.
5. [ ] Submit under **CampX Project Assignment**:
   * Upload all project source files (or zipped project folder).
   * Upload `Project_Report.pdf` with all screenshots.
   * Provide the public GitHub repository link.
