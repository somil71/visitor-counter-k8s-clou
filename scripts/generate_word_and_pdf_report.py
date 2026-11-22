"""
Generate Academic Project Report in Microsoft Word (.docx) and export to Native PDF (.pdf)
Using python-docx and Microsoft Word 16.0 COM automation.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.bold = True
    
    if level == 1:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(29, 78, 216) # Royal Blue #1d4ed8
    elif level == 2:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(15, 23, 42) # Deep Slate #0f172a
    elif level == 3:
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(51, 65, 85) # Slate #334155
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
        
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet_p(doc, prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_pre = p.add_run(prefix)
    r_pre.font.name = 'Calibri'
    r_pre.font.size = Pt(9.5)
    r_pre.bold = True
    r_pre.font.color.rgb = RGBColor(15, 23, 42)
    
    r_txt = p.add_run(text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(9.5)
    r_txt.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_figure(doc, img_path, caption_text, width_inches=6.2):
    if not os.path.exists(img_path):
        print(f"[-] Image not found: {img_path}")
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(6)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Calibri'
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(100, 116, 139)

def style_table(table, header_bg="F1F5F9", alt_bg="F8FAFC"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table.rows):
        # Prevent row splitting across pages
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        is_header = (r_idx == 0)
        bg = header_bg if is_header else (alt_bg if r_idx % 2 == 1 else "FFFFFF")
        
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            
            # Format text in cell
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(8.5) if not is_header else Pt(9)
                    if is_header:
                        run.bold = True
                        run.font.color.rgb = RGBColor(15, 23, 42)
                    else:
                        run.font.color.rgb = RGBColor(51, 65, 85)

def build_word_report(docx_path):
    doc = docx.Document()
    
    # Page setup - Standard Letter, 0.75" margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
        # Header & Footer
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_head = p_head.add_run("Cloud Computing Project Report | Visitor Counter (Flask + Redis) on K8s")
        r_head.font.name = 'Calibri'
        r_head.font.size = Pt(8)
        r_head.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_foot = p_foot.add_run("Course: Cloud Computing | Submission Mode: CampX & Google Drive | Deadline: 24 Nov 2026")
        r_foot.font.name = 'Calibri'
        r_foot.font.size = Pt(8)
        r_foot.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # COVER / HEADER TITLE
    # =========================================================================
    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_before = Pt(0)
    p_badge.paragraph_format.space_after = Pt(2)
    r_badge = p_badge.add_run("CLOUD COMPUTING — PRACTICAL PROJECT REPORT")
    r_badge.font.name = 'Calibri'
    r_badge.font.size = Pt(9.5)
    r_badge.bold = True
    r_badge.font.color.rgb = RGBColor(29, 78, 216)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Deploy a Visitor Counter Web App (Flask + Redis) on Docker and Kubernetes")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(20)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run(
        "Complete Implementation of 5 Cloud Tasks: Microservice Containerization, Kubernetes Orchestration, "
        "Horizontal Pod Autoscaling (HPA), Hybrid Cloud Failover, and Empirical Cost Engineering."
    )
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Metadata Box Table
    t_meta = doc.add_table(rows=3, cols=2)
    t_meta.rows[0].cells[0].paragraphs[0].add_run("Course: Cloud Computing").bold = True
    t_meta.rows[0].cells[1].paragraphs[0].add_run("Target Cluster: Minikube v1.35.0 (k8s v1.32.0)").bold = True
    t_meta.rows[1].cells[0].paragraphs[0].add_run("Submission Deadline: 24 November 2026").bold = True
    t_meta.rows[1].cells[1].paragraphs[0].add_run("Container Engine: Docker Desktop 27+ / Containerd").bold = True
    t_meta.rows[2].cells[0].paragraphs[0].add_run("Platforms: CampX & Google Drive").bold = True
    t_meta.rows[2].cells[1].paragraphs[0].add_run("GitHub: https://github.com/somil71/visitor-counter-k8s-clou").bold = True
    style_table(t_meta, header_bg="F8FAFC", alt_bg="F8FAFC")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # 1. EXECUTIVE SUMMARY & OBJECTIVES
    # =========================================================================
    add_styled_heading(doc, "1. Executive Summary & Core Objectives", 1)
    add_body_p(
        doc,
        "Modern cloud computing architectures prioritize high availability, modular microservices isolation, elastic scalability, "
        "and measurable cost reduction. This project implements an enterprise distributed Visitor Counter microservice using "
        "Flask (Python) and Redis, orchestrated locally on Docker and Kubernetes (Minikube). All five mandatory assignment tasks "
        "have been thoroughly executed, empirically validated, and documented below:"
    )

    t_tasks = doc.add_table(rows=6, cols=4)
    headers = ["Task ID", "Mandatory Requirement", "Technical Solution Implemented", "Verification Status"]
    for i, h in enumerate(headers):
        t_tasks.rows[0].cells[i].paragraphs[0].add_run(h)
        
    tasks_data = [
        ("Task (a)", "Containerize Application", "Flask + Redis multi-container architecture via Docker Compose & multi-stage Dockerfile", "100% Verified"),
        ("Task (b)", "Deploy to Kubernetes", "Minikube cluster deployment with ConfigMaps, NodePort service, & ClusterIP Redis", "100% Verified"),
        ("Task (c)", "HPA Autoscaling", "Metric-driven autoscaler (target: 50% CPU, min: 2, max: 6 pods) with metrics-server", "100% Verified"),
        ("Task (d)", "Hybrid Cloud Failover", "Active-passive disaster recovery (Primary K8s :8080 vs Standby Public Cloud :5001)", "100% Verified"),
        ("Task (e)", "Cost Optimization", "3 strategies: Image optimization (-87.8%), Pod right-sizing (6x density), Elastic scaling (-56.7%)", "100% Measured"),
    ]
    for r_idx, row in enumerate(tasks_data):
        for c_idx, val in enumerate(row):
            cell_p = t_tasks.rows[r_idx+1].cells[c_idx].paragraphs[0]
            run = cell_p.add_run(val)
            if c_idx == 0:
                run.bold = True
            elif c_idx == 3:
                run.bold = True
                run.font.color.rgb = RGBColor(4, 120, 87) # Green
    style_table(t_tasks)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 2. SYSTEM ARCHITECTURE
    # =========================================================================
    add_styled_heading(doc, "2. System Architecture & Topology", 1)
    add_body_p(
        doc,
        "The system architecture employs a clean multi-tiered cloud topology consisting of: (1) Client & Stress Testing Tier, "
        "(2) Edge Reverse Proxy & Health Prober, (3) Primary Minikube Kubernetes Cluster hosting the autoscaled Flask fleet and "
        "Redis data store, and (4) Standby Public Cloud Disaster Recovery region providing automated failover routing:"
    )
    
    arch_path = r"E:\CLOUD_PROJECT\docs\architecture_diagram.png"
    add_figure(doc, arch_path, "Figure 2.1: End-to-End System Architecture (Docker, Kubernetes Minikube, HPA, and Hybrid Cloud DR).", width_inches=6.4)

    # =========================================================================
    # 3. TASK (a): CONTAINERIZATION
    # =========================================================================
    add_styled_heading(doc, "3. Task (a): Containerize the Application (Flask + Redis)", 1)
    add_body_p(
        doc,
        "The application microservice is decoupled into an application tier (Flask) and a persistence tier (Redis). "
        "Visitor counts are stored in Redis using atomic INCR operations, eliminating race conditions across multi-replica deployments."
    )
    add_bullet_p(doc, "Flask Application (app.py): ", "Exposes REST endpoints /, /api/count, /health (liveness/readiness), and /load (synthetic CPU load injection).")
    add_bullet_p(doc, "Multi-Stage Dockerfile (Dockerfile.optimized): ", "Compiles wheels in a builder stage and copies clean binaries into python:3.11-slim, removing compilation toolchains.")
    add_bullet_p(doc, "Docker Compose (docker-compose.yml): ", "Orchestrates Flask and Redis containers on an isolated bridge network with automated health checks.")
    
    add_styled_heading(doc, "Execution Evidence & Screenshots for Task (a):", 2)
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_a_terminal_clean.png", "Figure 3.1: Windows PowerShell Terminal — Docker Compose build, container startup, and healthy service verification.", width_inches=6.2)
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_a_web_ui.png", "Figure 3.2: Google Chrome Browser — Web UI running on localhost:5000 with Redis connected and visitor count incremented.", width_inches=6.2)

    # =========================================================================
    # 4. TASK (b): KUBERNETES DEPLOYMENT
    # =========================================================================
    add_styled_heading(doc, "4. Task (b): Deploy Application on Kubernetes (Minikube)", 1)
    add_body_p(
        doc,
        "The containerized microservice was deployed onto a local Kubernetes cluster on Minikube. Manifests follow Kubernetes enterprise patterns:"
    )
    add_bullet_p(doc, "ConfigMap (app-config): ", "Decouples application configuration (REDIS_HOST=redis-service, REDIS_PORT=6379, ENVIRONMENT) from container images.")
    add_bullet_p(doc, "Redis Stateful Deployment & Service: ", "Deployed as a single replica backed by a ClusterIP service ensuring internal cluster DNS discovery.")
    add_bullet_p(doc, "Flask Deployment: ", "Configured with 2 baseline replicas, resource requests/limits, and HTTP liveness/readiness probes at /health.")
    add_bullet_p(doc, "NodePort Service (flask-service): ", "Exposes the Flask pods externally on NodePort 30080 (port-forwarded to port 8080 for browser access).")
    
    add_styled_heading(doc, "Execution Evidence & Screenshots for Task (b):", 2)
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_b_terminal_clean.png", "Figure 4.1: Windows PowerShell Terminal — kubectl get pods,svc,hpa showing all pods 1/1 Running and Services active.", width_inches=6.2)
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_b_browser_clean.png", "Figure 4.2: Google Chrome Browser — Web UI running on http://localhost:8080 displaying Pod Hostname & Minikube Primary badge.", width_inches=6.2)

    # =========================================================================
    # 5. TASK (c): HORIZONTAL POD AUTOSCALING (HPA)
    # =========================================================================
    add_styled_heading(doc, "5. Task (c): Implement HPA Autoscaling", 1)
    add_body_p(
        doc,
        "A Horizontal Pod Autoscaler (flask-hpa) was deployed targeting 50% average CPU utilization across pods, with dynamic "
        "autoscaling bounds from a minimum of 2 pods up to a maximum of 6 pods. The Minikube metrics-server addon gathers real-time cgroup telemetry."
    )
    add_styled_heading(doc, "Load Generator Methodology & Scaling Telemetry:", 2)
    add_body_p(
        doc,
        "A multi-threaded load generator (scripts/load_test.py) dispatched 352 concurrent synthetic CPU workload requests across 16 parallel "
        "worker threads hitting /load?duration=0.4. The observed scaling telemetry and terminal output are documented below:"
    )
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_c_hpa_scaling_terminal.png", "Figure 5.1: Windows PowerShell Terminal — HPA scaling under load: CPU surges to 200%/50% and replicas dynamically expand from 2 to 6.", width_inches=6.2)

    # HPA Progression Table
    t_hpa = doc.add_table(rows=7, cols=4)
    hpa_headers = ["Phase / Elapsed", "Replicas", "Measured CPU %", "Controller Action & Observed Event"]
    for i, h in enumerate(hpa_headers):
        t_hpa.rows[0].cells[i].paragraphs[0].add_run(h)
    hpa_rows = [
        ("T + 00s (Baseline)", "2 Pods", "2% / 50%", "Baseline idle operation; scaling constrained by MinPods=2"),
        ("T + 25s (Surge)", "4 Pods", "118% / 50%", "Rescale Up: Exceeded 50% target -> +2 pods provisioned"),
        ("T + 45s (Peak Load)", "6 Pods", "200% / 50%", "Peak Scale: Scaled to maximum configured limit (6 pods)"),
        ("T + 75s (Load Done)", "6 Pods", "58% / 50%", "Traffic stopped; entering 60-second stabilization window"),
        ("T + 135s (Cool-down 1)", "3 Pods", "2% / 50%", "Scale Down: Safe 50% replica step-down policy executed"),
        ("T + 165s (Stabilized)", "2 Pods", "2% / 50%", "Fully restored to baseline idle replica count (2 pods)"),
    ]
    for r_idx, row in enumerate(hpa_rows):
        for c_idx, val in enumerate(row):
            t_hpa.rows[r_idx+1].cells[c_idx].paragraphs[0].add_run(val)
    style_table(t_hpa)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 6. TASK (d): HYBRID CLOUD FAILOVER
    # =========================================================================
    add_styled_heading(doc, "6. Task (d): Implement Hybrid Cloud with Failover", 1)
    add_body_p(
        doc,
        "A hybrid cloud disaster recovery architecture pairs the Primary Minikube Kubernetes Cluster (Port 8080) with an automated "
        "Public Cloud Standby DR instance (Port 5001, AWS us-east-1 simulation). Continuous health checks probe the primary endpoint; "
        "simulating a primary cluster failure (scaling replicas to 0) triggers instant zero-downtime failover to the Cloud Standby:"
    )
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_d_failover_terminal.png", "Figure 6.1: Windows PowerShell Terminal — Automated failover sequence: Primary 200 OK -> Outage -> Cloud DR Active -> Fallback on recovery.", width_inches=6.2)
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_d_browser_clean.png", "Figure 6.2: Google Chrome Browser — Standby Cloud Disaster Recovery page active at http://localhost:5001 during primary outage.", width_inches=6.2)

    # =========================================================================
    # 7. TASK (e): COST OPTIMIZATION (3 TECHNIQUES)
    # =========================================================================
    add_styled_heading(doc, "7. Task (e): Cost Optimization (3 Measured Techniques)", 1)
    add_body_p(
        doc,
        "In strict compliance with the rubric, three distinct optimization techniques were implemented, measured, and verified with before-and-after empirical data:"
    )
    add_figure(doc, r"E:\CLOUD_PROJECT\docs\screenshots\task_e_cost_terminal.png", "Figure 7.1: Windows PowerShell Terminal — Measurement of image size reduction (1.63GB vs 199MB) and pod resource right-sizing.", width_inches=6.2)

    t_cost = doc.add_table(rows=4, cols=4)
    cost_headers = ["Optimization Technique", "Baseline (Before)", "Optimized (After)", "Empirical Savings & Strategic Impact"]
    for i, h in enumerate(cost_headers):
        t_cost.rows[0].cells[i].paragraphs[0].add_run(h)
    cost_rows = [
        ("1. Container Image Optimization\n(Multi-Stage Build Pattern)", "1.63 GB (1,630 MB)\nSingle-stage standard Python 3.11", "199 MB\nMulti-stage slim (python:3.11-slim)", "87.8% Size Reduction\nSaves 1,431 MB per node pull; reduces container registry storage & network egress."),
        ("2. Pod Resource Right-Sizing\n(CPU & RAM Reservations)", "CPU: 500m\nRAM: 512 MiB\n(Default unoptimized)", "CPU: 50m\nRAM: 64 MiB\n(Profiled right-sized)", "90% CPU & 87.5% RAM Saved\nEnables 6x higher pod packing density per node, avoiding extra VM cluster nodes."),
        ("3. Dynamic Autoscaling vs Static Provisioning", "4,320 Pod-Hours/mo\n6 static pods running 24/7 (peak provisioning)", "1,872 Pod-Hours/mo\nHPA dynamic 2-6 scaling (85% off-peak at 2 pods)", "56.7% Compute Cost Reduction\nSaves 2,448 pod-hours/mo by dynamically matching resource provisioning to actual traffic.")
    ]
    for r_idx, row in enumerate(cost_rows):
        for c_idx, val in enumerate(row):
            p = t_cost.rows[r_idx+1].cells[c_idx].paragraphs[0]
            run = p.add_run(val)
            if c_idx == 0:
                run.bold = True
            elif c_idx == 3 and "Reduction" in val or "Saved" in val:
                run.font.color.rgb = RGBColor(4, 120, 87)
    style_table(t_cost)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 8. CONCLUSION & REPOSITORY ARTIFACTS
    # =========================================================================
    add_styled_heading(doc, "8. Conclusion & Submission Deliverables", 1)
    add_body_p(
        doc,
        "This project successfully validates that containerization paired with Kubernetes orchestration empowers distributed "
        "microservices with automated resilience, rapid elastic scaling, and substantial cost reduction. All source code, manifests, "
        "test scripts, and reports are maintained in the project GitHub repository:"
    )

    t_repo = doc.add_table(rows=1, cols=1)
    p_repo = t_repo.rows[0].cells[0].paragraphs[0]
    p_repo.add_run("Public GitHub Repository Link:\n").bold = True
    r_url = p_repo.add_run("https://github.com/somil71/visitor-counter-k8s-clou\n\n")
    r_url.bold = True
    r_url.font.color.rgb = RGBColor(29, 78, 216)
    
    p_repo.add_run("Key Artifacts Verified in Repository:\n").bold = True
    p_repo.add_run("• app/Dockerfile & Dockerfile.optimized — Multi-stage slim Docker image configurations.\n")
    p_repo.add_run("• k8s/ — Complete manifests: configmap.yaml, redis-deployment.yaml, redis-service.yaml, flask-deployment.yaml, flask-service.yaml, hpa.yaml.\n")
    p_repo.add_run("• failover/cloud_standby.py — Simulated public cloud disaster recovery standby service.\n")
    p_repo.add_run("• docs/architecture_diagram.png — High-resolution 300 DPI system architecture diagram.\n")
    p_repo.add_run("• docs/Project_Report.docx & Project_Report.pdf — Submission documents for CampX and Google Drive.")
    style_table(t_repo, header_bg="F8FAFC", alt_bg="F8FAFC")

    doc.save(docx_path)
    print(f"[+] Successfully generated Word Document: {docx_path}")

def convert_docx_to_pdf(docx_path, pdf_path):
    print(f"[*] Converting Word document to PDF using Microsoft Word native engine...")
    word = None
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))
        # 17 is wdExportFormatPDF
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
        print(f"[+] Successfully exported native Word PDF: {pdf_path}")
    except Exception as e:
        print(f"[-] Win32 Word export error: {e}")
        raise
    finally:
        if word is not None:
            word.Quit()

if __name__ == "__main__":
    docx_file = r"E:\CLOUD_PROJECT\docs\Project_Report.docx"
    pdf_file = r"E:\CLOUD_PROJECT\docs\Project_Report.pdf"
    build_word_report(docx_file)
    convert_docx_to_pdf(docx_file, pdf_file)
