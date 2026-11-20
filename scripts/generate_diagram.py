"""
Generate Publication-Quality System Architecture Diagram
for Distributed Visitor Counter on Docker & Kubernetes
Produces both high-res PNG (300 DPI) and vector SVG.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arrow

def create_architecture_diagram():
    fig = plt.figure(figsize=(16, 11), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    # Color Palette
    PRIMARY_COLOR = '#38bdf8'      # Cyan
    SECONDARY_COLOR = '#818cf8'    # Indigo
    ACCENT_GREEN = '#34d399'       # Emerald
    ACCENT_RED = '#f87171'         # Red (Standby)
    ACCENT_AMBER = '#fbbf24'       # Amber (Metrics / HPA)
    CONTAINER_BG = '#1e293b'       # Slate 800
    SUB_CONTAINER = '#334155'      # Slate 700
    TEXT_LIGHT = '#f8fafc'
    TEXT_MUTED = '#94a3b8'

    # Title & Header
    ax.text(8.0, 10.4, "Distributed Visitor Counter - System Architecture", 
            fontsize=20, fontweight='bold', color=TEXT_LIGHT, ha='center', va='center')
    ax.text(8.0, 10.0, "Multi-Container Cloud Native Deployment with Kubernetes HPA & Hybrid Cloud Failover", 
            fontsize=11, color=TEXT_MUTED, ha='center', va='center')

    # Helper function to draw rounded boxes
    def draw_box(x, y, w, h, bg_color, border_color, border_width=1.5, radius=0.2, linestyle='-'):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad={radius},rounding_size=0.25",
                             facecolor=bg_color, edgecolor=border_color,
                             linewidth=border_width, linestyle=linestyle, zorder=2)
        ax.add_patch(box)
        return box

    # 1. CLIENT TIER (Top)
    draw_box(4.5, 8.6, 7.0, 0.9, CONTAINER_BG, PRIMARY_COLOR, border_width=2.0)
    ax.text(8.0, 9.15, "CLIENT TRAFFIC & TESTING HARNESS", fontsize=11, fontweight='bold', color=PRIMARY_COLOR, ha='center')
    ax.text(8.0, 8.8, "Web Browsers  |  REST API Calls (:5000 / :8080)  |  HPA Load Generator (16 Threads)", 
            fontsize=9.5, color=TEXT_LIGHT, ha='center')

    # 2. EDGE / TRAFFIC ROUTER (Middle Top)
    draw_box(5.0, 7.1, 6.0, 0.9, CONTAINER_BG, ACCENT_AMBER, border_width=2.0)
    ax.text(8.0, 7.65, "EDGE LOAD BALANCER & REVERSE PROXY", fontsize=11, fontweight='bold', color=ACCENT_AMBER, ha='center')
    ax.text(8.0, 7.3, "Health Monitor & Traffic Director  |  Primary / Failover Standby Switching", 
            fontsize=9, color=TEXT_LIGHT, ha='center')

    # Arrow Client -> Traffic Router
    ax.annotate('', xy=(8.0, 8.05), xytext=(8.0, 8.55),
                arrowprops=dict(facecolor=TEXT_LIGHT, edgecolor=TEXT_LIGHT, width=2, headwidth=8, shrink=0.05))

    # 3. PRIMARY ZONE: KUBERNETES CLUSTER (Left Main Box)
    draw_box(0.6, 0.5, 10.2, 5.9, '#111e38', PRIMARY_COLOR, border_width=2.5)
    ax.text(5.7, 6.15, "PRIMARY REGION: LOCAL KUBERNETES CLUSTER (Minikube)", 
            fontsize=12, fontweight='bold', color=PRIMARY_COLOR, ha='center')

    # Ingress / NodePort Service
    draw_box(3.2, 5.0, 5.0, 0.7, SUB_CONTAINER, PRIMARY_COLOR, border_width=1.5)
    ax.text(5.7, 5.35, "Kubernetes Service: flask-service (NodePort :30080 / :8080)", 
            fontsize=9.5, fontweight='bold', color=TEXT_LIGHT, ha='center')

    # Left to Primary Cluster arrow
    ax.annotate('', xy=(5.7, 5.75), xytext=(7.0, 7.05),
                arrowprops=dict(facecolor=PRIMARY_COLOR, edgecolor=PRIMARY_COLOR, width=2.5, headwidth=9, shrink=0.05))
    ax.text(5.6, 6.6, "Active Primary Traffic", fontsize=9, fontweight='bold', color=PRIMARY_COLOR, rotation=35)

    # ConfigMap Box (Left side of K8s)
    draw_box(1.0, 3.6, 2.5, 1.1, SUB_CONTAINER, SECONDARY_COLOR, border_width=1.5)
    ax.text(2.25, 4.35, "ConfigMap", fontsize=10, fontweight='bold', color=SECONDARY_COLOR, ha='center')
    ax.text(2.25, 3.9, "app-config\nREDIS_HOST=redis-service\nREDIS_PORT=6379", 
            fontsize=7.5, color=TEXT_LIGHT, ha='center', va='center')

    # HPA Controller & Metrics Server (Right side of K8s)
    draw_box(7.9, 3.5, 2.6, 1.3, SUB_CONTAINER, ACCENT_AMBER, border_width=1.5)
    ax.text(9.2, 4.45, "HPA & Metrics-Server", fontsize=10, fontweight='bold', color=ACCENT_AMBER, ha='center')
    ax.text(9.2, 3.9, "Target: CPU 50%\nMin: 2 Pods | Max: 6 Pods\nScrape: metrics.k8s.io", 
            fontsize=7.5, color=TEXT_LIGHT, ha='center', va='center')

    # Flask Deployment Box (Center of K8s)
    draw_box(3.8, 2.8, 3.8, 1.9, CONTAINER_BG, ACCENT_GREEN, border_width=2.0)
    ax.text(5.7, 4.4, "Deployment: flask-deployment", fontsize=10.5, fontweight='bold', color=ACCENT_GREEN, ha='center')
    
    # 3 Pod Icons inside Flask Deployment
    for idx, name in enumerate(["Pod 1 (Active)", "Pod 2 (Active)", "Pods 3-6 (HPA)"]):
        py = 3.85 - idx * 0.45
        draw_box(4.0, py, 3.4, 0.35, SUB_CONTAINER, ACCENT_GREEN, border_width=1.0)
        ax.text(5.7, py + 0.17, name, fontsize=8, color=TEXT_LIGHT, ha='center', va='center')

    # Arrow Service -> Deployment
    ax.annotate('', xy=(5.7, 4.75), xytext=(5.7, 4.95),
                arrowprops=dict(facecolor=ACCENT_GREEN, edgecolor=ACCENT_GREEN, width=1.5, headwidth=6))

    # Arrow ConfigMap -> Deployment
    ax.annotate('', xy=(3.75, 3.75), xytext=(3.55, 4.15),
                arrowprops=dict(facecolor=SECONDARY_COLOR, edgecolor=SECONDARY_COLOR, width=1.2, headwidth=5))

    # Arrow HPA -> Deployment
    ax.annotate('', xy=(7.65, 3.75), xytext=(7.85, 4.15),
                arrowprops=dict(facecolor=ACCENT_AMBER, edgecolor=ACCENT_AMBER, width=1.2, headwidth=5))

    # Redis Service & Pod (Bottom of K8s)
    draw_box(2.2, 0.8, 7.0, 1.4, SUB_CONTAINER, '#e2e8f0', border_width=1.5)
    ax.text(5.7, 1.9, "REDIS IN-MEMORY KEY-VALUE DATA STORE", fontsize=10, fontweight='bold', color='#e2e8f0', ha='center')
    
    draw_box(2.5, 1.0, 3.0, 0.65, CONTAINER_BG, '#e2e8f0', border_width=1.0)
    ax.text(4.0, 1.32, "Service: redis-service\nClusterIP :6379", fontsize=8, color=TEXT_LIGHT, ha='center', va='center')

    draw_box(5.9, 1.0, 3.0, 0.65, CONTAINER_BG, '#e2e8f0', border_width=1.0)
    ax.text(7.4, 1.32, "Pod: redis-deployment\nImage: redis:7-alpine", fontsize=8, color=TEXT_LIGHT, ha='center', va='center')

    # Arrow Flask -> Redis
    ax.annotate('', xy=(5.7, 2.25), xytext=(5.7, 2.75),
                arrowprops=dict(facecolor='#e2e8f0', edgecolor='#e2e8f0', width=1.5, headwidth=6))
    ax.text(5.85, 2.5, "Atomic Counter (INCR)", fontsize=7.5, color=TEXT_MUTED)

    # 4. SECONDARY ZONE: PUBLIC CLOUD DISASTER RECOVERY (Right Main Box)
    draw_box(11.4, 1.8, 4.0, 4.6, '#2a1515', ACCENT_RED, border_width=2.5, linestyle='--')
    ax.text(13.4, 6.15, "SECONDARY REGION (STANDBY DR)", fontsize=11, fontweight='bold', color=ACCENT_RED, ha='center')
    ax.text(13.4, 5.85, "Public Cloud (AWS us-east-1)", fontsize=9, color=TEXT_MUTED, ha='center')

    draw_box(11.8, 3.8, 3.2, 1.6, CONTAINER_BG, ACCENT_RED, border_width=1.5)
    ax.text(13.4, 5.0, "Cloud Standby Server", fontsize=10, fontweight='bold', color=ACCENT_RED, ha='center')
    ax.text(13.4, 4.4, "Python / Flask Service (:5001)\nAutomated Health Check\nInstant Failover Target", 
            fontsize=8, color=TEXT_LIGHT, ha='center', va='center')

    draw_box(11.8, 2.2, 3.2, 1.1, CONTAINER_BG, '#e2e8f0', border_width=1.0)
    ax.text(13.4, 2.9, "State Backup / Fallback", fontsize=9, fontweight='bold', color='#e2e8f0', ha='center')
    ax.text(13.4, 2.5, "Disaster Recovery Mode\nZero-Downtime Guarantee", fontsize=7.5, color=TEXT_MUTED, ha='center')

    # Failover Arrow from Traffic Router to Cloud Standby
    ax.annotate('', xy=(13.4, 5.45), xytext=(9.0, 7.05),
                arrowprops=dict(facecolor=ACCENT_RED, edgecolor=ACCENT_RED, width=2, headwidth=8, linestyle='--', shrink=0.05))
    ax.text(11.6, 6.6, "Failover on Outage", fontsize=8.5, fontweight='bold', color=ACCENT_RED, rotation=-25)

    # 5. BOTTOM BAR: COST OPTIMIZATION CALLOUTS
    draw_box(0.6, 0.05, 14.8, 0.35, CONTAINER_BG, '#38bdf8', border_width=1.0)
    ax.text(8.0, 0.22, 
            "Cost Optimization: [1] Multi-Stage Image (1.63 GB -> 199 MB, -87.8%)  |  [2] Right-Sizing (50m CPU / 64Mi RAM, 6x Density)  |  [3] HPA Dynamic Scaling (-56.7% pod-hrs)", 
            fontsize=8, fontweight='bold', color='#38bdf8', ha='center', va='center')

    plt.tight_layout()
    plt.savefig(r'E:\CLOUD_PROJECT\docs\architecture_diagram.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.savefig(r'E:\CLOUD_PROJECT\docs\architecture_diagram.svg', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print("[+] Architecture diagrams generated successfully:")
    print("    - E:\\CLOUD_PROJECT\\docs\\architecture_diagram.png (High-Res 300 DPI)")
    print("    - E:\\CLOUD_PROJECT\\docs\\architecture_diagram.svg (Vector Format)")

if __name__ == '__main__':
    create_architecture_diagram()
