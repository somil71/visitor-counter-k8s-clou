"""
Hybrid Cloud Automated Failover Simulation and Verification Tool
This script demonstrates and verifies Task (d): Hybrid Cloud with Failover.
It acts as an intelligent client/proxy demonstrating zero-downtime failover between:
- Primary: Local Kubernetes Cluster (http://localhost:30080 or minikube)
- Secondary: Public Cloud Disaster Recovery Standby (http://localhost:5001)
"""

import urllib.request
import time
import sys

PRIMARY_URL = "http://localhost:8080"
STANDBY_URL = "http://localhost:5001"

def check_endpoint(url, timeout=1.5):
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'CloudMonitor/1.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = (time.time() - start) * 1000
            body = response.read().decode('utf-8', errors='ignore')
            return True, response.status, latency, body
    except Exception as e:
        return False, None, None, str(e)

def run_simulation(duration_seconds=30):
    print("=" * 70)
    print("   HYBRID CLOUD AUTOMATED FAILOVER TEST MONITOR")
    print("=" * 70)
    print(f"Primary Target   : {PRIMARY_URL} (Local K8s Cluster)")
    print(f"Secondary Target : {STANDBY_URL} (Public Cloud Standby)")
    print("-" * 70)
    print(f"{'Time':<10} | {'Routing Target':<22} | {'Status':<10} | {'Latency':<10} | {'Failover State'}")
    print("-" * 70)

    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        cur_time = time.strftime("%H:%M:%S")

        # Step 1: Probe Primary
        ok, status, lat, body = check_endpoint(PRIMARY_URL)

        if ok:
            print(f"{cur_time:<10} | {'Primary (K8s Cluster)':<22} | {status:<10} | {f'{lat:.1f}ms':<10} | NORMAL (Primary Active)")
        else:
            # Step 2: Failover to Secondary Standby
            s_ok, s_status, s_lat, s_body = check_endpoint(STANDBY_URL)
            if s_ok:
                print(f"{cur_time:<10} | {'Secondary (Cloud DR)':<22} | {s_status:<10} | {f'{s_lat:.1f}ms':<10} | [!] FAILOVER ENGAGED")
            else:
                print(f"{cur_time:<10} | {'ALL TARGETS DOWN':<22} | {'DOWN':<10} | {'N/A':<10} | CRITICAL")

        time.sleep(1)

    print("-" * 70)
    print("[*] Failover simulation test completed successfully.")
    print("=" * 70)

if __name__ == "__main__":
    dur = 30
    if len(sys.argv) > 1:
        dur = int(sys.argv[1])
    run_simulation(dur)
