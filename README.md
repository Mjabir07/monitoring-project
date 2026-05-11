# Sentinel AI - Observability & AIOps Engine (V2)

## Architecture Overview
Sentinel V2 is a fully containerized, Kubernetes-native observability platform. It is designed as a Hub-and-Spoke architecture to monitor both internal server infrastructure and external web assets, enhanced by a local LLM for automated incident reporting.

## Core Infrastructure
* **Orchestration:** K3s (Lightweight Kubernetes)
* **Metrics Database:** Prometheus (kube-prometheus-stack)
* **Visualization:** Grafana (Exposed via Cloudflare Zero Trust)
* **Internal Telemetry:** Node Exporter (Hardware Metrics)
* **External Telemetry:** Prometheus Blackbox Exporter (HTTP/SSL/DNS Probing)
* **AIOps:** Custom Python Flask Webhook bridged to local Phi-3 LLM

## Key Configuration Files
* `sentinel-values.yaml`: Helm overrides for Grafana/Prometheus (Admin passwords, NodePorts).
* `external-targets.yaml`: Kubernetes Probe targets for the Blackbox Exporter.
* `Dockerfile` & `requirements.txt`: Build instructions for the AI Webhook.
* `ai-bridge.py`: The Python Flask application that translates Prometheus alerts into Phi-3 prompts.
* `ai-bridge-deployment.yaml`: The Kubernetes manifest deploying the AI bridge into the cluster.

## Version
Current Release: **v2.0.0 (Backend Engine Locked)**
