"""
Load Generator Script to Trigger Kubernetes HPA Autoscaling
Sends concurrent requests to the Flask visitor counter /load endpoint
to increase CPU utilization and verify HPA scaling.
"""

import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

TARGET_URL = "http://localhost:8080/load?duration=0.4"

def make_request(req_id):
    try:
        start = time.time()
        with urllib.request.urlopen(TARGET_URL, timeout=5) as response:
            latency = time.time() - start
            return True, response.status, latency
    except Exception as e:
        return False, str(e), 0

def run_load_test(threads=10, duration_seconds=60):
    print("=" * 65)
    print("      KUBERNETES HPA AUTOSCALING LOAD TEST GENERATOR")
    print("=" * 65)
    print(f"Target URL         : {TARGET_URL}")
    print(f"Concurrent Workers : {threads}")
    print(f"Duration           : {duration_seconds} seconds")
    print("Run in another terminal: 'kubectl get hpa -w' or 'kubectl get pods -w'")
    print("-" * 65)

    start_time = time.time()
    total_requests = 0
    successful_requests = 0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        while time.time() - start_time < duration_seconds:
            futures = [executor.submit(make_request, i) for i in range(threads)]
            for f in futures:
                ok, status, lat = f.result()
                total_requests += 1
                if ok:
                    successful_requests += 1
            
            elapsed = time.time() - start_time
            print(f"[{time.strftime('%H:%M:%S')}] Elapsed: {int(elapsed)}s | Requests sent: {total_requests} (Success: {successful_requests})", end="\r")
            time.sleep(0.1)

    print("\n" + "-" * 65)
    print(f"[*] Load test completed!")
    print(f"Total Requests Sent   : {total_requests}")
    print(f"Successful Responses  : {successful_requests}")
    print(f"Success Rate          : {(successful_requests / max(1, total_requests)) * 100:.1f}%")
    print("=" * 65)

if __name__ == "__main__":
    workers = 12
    duration = 60
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    if len(sys.argv) > 2:
        workers = int(sys.argv[2])
    run_load_test(workers, duration)
