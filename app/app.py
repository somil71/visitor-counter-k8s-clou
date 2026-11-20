import os
import socket
import time
import math
from flask import Flask, render_template, jsonify, request
import redis

app = Flask(__name__)

# Configuration via Environment Variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
ENVIRONMENT = os.getenv("ENVIRONMENT_NAME", "On-Premises / Primary Kubernetes Cluster")
CLOUD_REGION = os.getenv("CLOUD_REGION", "local-minikube-node-01")

# Initialize Redis client with connection pooling & retries
def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        socket_timeout=2,
        socket_connect_timeout=2,
        decode_responses=True
    )

@app.route("/")
def index():
    hostname = socket.gethostname()
    visits = "N/A"
    redis_status = "Disconnected"
    error_message = None

    try:
        r = get_redis_client()
        visits = r.incr("visitor_count")
        redis_status = "Connected"
    except Exception as e:
        error_message = str(e)
        redis_status = "Error: " + str(e)

    return render_template(
        "index.html",
        visits=visits,
        hostname=hostname,
        redis_status=redis_status,
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        environment=ENVIRONMENT,
        cloud_region=CLOUD_REGION,
        error_message=error_message
    )

@app.route("/health")
def health():
    """Health check endpoint for Kubernetes liveness & readiness probes."""
    hostname = socket.gethostname()
    redis_healthy = False
    try:
        r = get_redis_client()
        redis_healthy = bool(r.ping())
    except Exception:
        redis_healthy = False

    status = {
        "status": "healthy" if redis_healthy else "degraded",
        "hostname": hostname,
        "environment": ENVIRONMENT,
        "redis_connected": redis_healthy,
        "timestamp": time.time()
    }
    # Return 200 even if redis is degraded so app stays up, or 503 if strict
    return jsonify(status), 200

@app.route("/api/count")
def api_count():
    """REST API endpoint returning JSON visitor count."""
    try:
        r = get_redis_client()
        count = r.get("visitor_count") or 0
        return jsonify({"count": int(count), "hostname": socket.gethostname()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/load")
def cpu_load():
    """
    Simulated CPU load endpoint to easily test Horizontal Pod Autoscaler (HPA).
    Runs floating point operations for a specified duration (default: 0.25s).
    """
    duration = float(request.args.get("duration", 0.25))
    duration = min(duration, 2.0) # cap to 2 seconds max per request
    start = time.time()
    result = 0.0
    while (time.time() - start) < duration:
        result += math.sqrt(12345.6789) * math.sin(9876.5432)

    return jsonify({
        "message": "Simulated CPU load completed",
        "duration_seconds": round(time.time() - start, 4),
        "pod_hostname": socket.gethostname()
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
