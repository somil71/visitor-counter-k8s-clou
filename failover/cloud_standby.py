"""
Simulated Secondary / Cloud Standby Instance for Hybrid Cloud Failover
This instance represents the disaster recovery backup running in a public cloud region (e.g., AWS us-east-1).
"""
import socket
import os
import time
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Failover Active</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #18181b;
            color: #f4f4f5;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #27272a;
            border: 2px solid #ef4444;
            border-radius: 12px;
            padding: 30px;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.2);
        }
        .tag {
            background: #ef4444;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        h1 { margin-top: 15px; color: #f87171; }
        .details { margin-top: 20px; text-align: left; background: #18181b; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <span class="tag">Disaster Recovery Engaged</span>
        <h1>Hybrid Cloud Failover Instance</h1>
        <p>Primary on-premises / local Kubernetes cluster is unreachable. Traffic automatically routed to Cloud Standby.</p>
        <div class="details">
            <p><strong>Environment:</strong> Public Cloud (AWS Standby)</p>
            <p><strong>Region:</strong> us-east-1</p>
            <p><strong>Instance Hostname:</strong> {{ hostname }}</p>
            <p><strong>Status:</strong> Active-Passive Backup Serving Traffic</p>
            <p><strong>Timestamp:</strong> {{ timestamp }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        hostname=socket.gethostname(),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "role": "disaster-recovery-standby",
        "cloud_provider": "AWS-Simulation",
        "region": "us-east-1"
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"[*] Cloud Standby Failover Server running on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
