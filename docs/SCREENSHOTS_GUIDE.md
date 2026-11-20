# Screenshot Guide for Submission Documentation

When submitting on CampX and Google Drive, your professor requires visual proof of execution for every task. Take the following screenshots and embed them into your final `Project_Report.docx` or `Project_Report.pdf`:

---

### Screenshot Checklist

#### Task (a): Containerize the Application
- [ ] **Screenshot 1.1:** Terminal output of `docker build -t visitor-app:baseline .` showing successful image build.
- [ ] **Screenshot 1.2:** Terminal output of `docker compose up -d` and `docker compose ps` showing both `flask-visitor-counter` and `redis-service` running in healthy state.
- [ ] **Screenshot 1.3:** Web browser opened at `http://localhost:5000` showing the Visitor Counter page with visits = 1, then refreshed to show visits = 2, with "Redis Status: Connected".

---

#### Task (b): Deploy Application on Kubernetes
- [ ] **Screenshot 2.1:** Terminal running `kubectl apply -f k8s/` or executing `scripts\2_k8s_deploy.ps1` showing creation of ConfigMap, Deployments, and Services.
- [ ] **Screenshot 2.2:** Terminal running `kubectl get pods -o wide`, `kubectl get deployments`, and `kubectl get svc` showing 2 healthy Flask pods and 1 Redis pod.
- [ ] **Screenshot 2.3:** Web browser opening the Kubernetes NodePort endpoint (`http://localhost:30080` or via `minikube service flask-service`) showing the app running from a Kubernetes Pod Hostname.

---

#### Task (c): Horizontal Pod Autoscaling (HPA)
- [ ] **Screenshot 3.1:** Terminal output of `kubectl get hpa flask-hpa` showing initial state: `TARGETS: 0%/50%`, `MINPODS: 2`, `MAXPODS: 6`, `REPLICAS: 2`.
- [ ] **Screenshot 3.2:** Split terminal: Left terminal running `python scripts/load_test.py`, Right terminal running `kubectl get hpa -w` and `kubectl get pods -w` showing CPU surging above 50% and pod replicas automatically scaling up to 4 or 6.
- [ ] **Screenshot 3.3:** Terminal showing HPA stabilization and gradual scale-down back to 2 replicas after load generation ends.

---

#### Task (d): Hybrid Cloud with Failover
- [ ] **Screenshot 4.1:** Architecture diagram of Hybrid Cloud (Primary Kubernetes Cluster vs. Standby Public Cloud).
- [ ] **Screenshot 4.2:** Normal State: Running `python scripts/3_failover_test.ps1` or browser hitting `http://localhost:30080` showing response from Primary K8s Cluster.
- [ ] **Screenshot 4.3:** Disaster State: Terminal command `kubectl scale deployment flask-deployment --replicas=0`, showing the monitor or browser instantly receiving responses from the Secondary Cloud Standby with zero downtime (`[!] FAILOVER ENGAGED`).
- [ ] **Screenshot 4.4:** Recovery State: Restoring `kubectl scale deployment flask-deployment --replicas=2`, traffic falling back to Primary.

---

#### Task (e): Cost Optimization
- [ ] **Screenshot 5.1 (Technique 1):** Terminal output of `docker images` showing `visitor-app:baseline` (1.02 GB) compared against `visitor-app:optimized` (126 MB) proving 87.6% size reduction.
- [ ] **Screenshot 5.2 (Technique 2):** Terminal output of `kubectl describe deployment flask-deployment` showing right-sized CPU requests (`50m`) and memory requests (`64Mi`).
- [ ] **Screenshot 5.3 (Technique 3):** Terminal output of HPA active metrics proving elastic pod hour savings compared to 24/7 static over-provisioning.
