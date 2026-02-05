# Cloud Native SOC Automation Platform (SIEM + SOAR)

An end‑to‑end **Cyber Security SOC & SOAR automation project** that detects security incidents using **SIEM (ELK Stack)** and performs **automated incident response** using **Python and Ansible**.

This project demonstrates how modern Security Operations Centers reduce response time by automating detection, decision‑making, and remediation.

---

## 📌 Project Overview

The objective of this project is to design and implement an **Automated Security Operations Center (SOC)** with **SOAR capabilities**.

The system:
- Collects logs from a target server
- Detects attacks using Kibana Security (SIEM)
- Automatically responds to confirmed threats
- Blocks malicious IPs without human intervention

The project is implemented in a **controlled lab environment** using multiple virtual machines.

---

## 🏗️ System Architecture

The architecture consists of **four isolated virtual machines**, each with a dedicated role.

flowchart LR
    A[Kali Linux Attacker VM] -->|Attack Traffic| B[Target Server SSH Nginx Auditd]
    B -->|Logs| C[Filebeat]
    C -->|Events| D[Logstash]
    D --> E[Elasticsearch]
    E --> F[Kibana Security]
    F -->|Alert| G[Python SOAR Script]
    G -->|Response| H[Ansible Playbook]
    H -->|Block IP| B


---

🖥️ Virtual Machine Roles
VM‑1: Target Server

- Ubuntu Linux
  
- SSH service
- Nginx web server
  
- Auditd (system auditing)
  
- Filebeat (log forwarding)

VM‑2: SOC / SIEM Server

- Elasticsearch (log storage)

- Logstash (log processing)

- Kibana (visualization)

- Kibana Security (detection engine)

VM‑3: Automation / SOAR Server

- Python (SOAR logic)

- Ansible (automated response)

- Cron (task scheduling)

VM‑4: Attacker Machine

- Kali Linux |
Used only for controlled attack simulation

---

🔄 Workflow Explanation

- Attacker initiates an attack (e.g., SSH brute force).

- Target server generates authentication and system logs.

- Filebeat forwards logs to Logstash.

- Logstash processes logs and sends them to Elasticsearch.

- Kibana Security evaluates logs using detection rules.

- A security alert is generated upon detection.

- Python SOAR script queries recent alerts.

- Ansible playbook blocks the attacker IP automatically.

- The incident is contained without manual intervention.

---
🚨 Attacks Simulated

- SSH Brute Force Attack
- Web Reconnaissance (Nginx access attempts)
- Port Scanning
- Privilege Escalation Attempts
- Abnormal Traffic Generation
---

⚙️ Technologies Used :

Elasticsearch | 
Logstash |
Kibana & Kibana Security |
Filebeat |
Python |
Ansible |
Linux (Ubuntu) |
Kali Linux |
SSH |
Nginx |
Auditd |
iptables |
Virtual Machines (VMware / VirtualBox)

🚀 How to Run (High Level)

- Configure Filebeat on the target server.
  
- Enable detection rules in Kibana Security.
  
- Simulate an attack from Kali Linux.
  
- Run the Python SOAR script (or schedule via cron).
  
- Verify that the attacker IP is automatically blocked.

