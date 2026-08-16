"""
Daily Telemetry & Engineering Activity Sync
Generates realistic engineering metrics, system telemetry, and structured
conventional commits matching the profile's Edge AI & Systems focus.
"""

import json
import os
import random
import sys
import urllib.request
from datetime import datetime, timezone

LOG_FILE = os.path.join("data", "engineering_log.json")
LAST_UPDATED_FILE = os.path.join("generated", "last_updated.txt")

TOPICS = [
    {
        "scope": "edge-ai",
        "type": "perf",
        "title": "optimize INT8 quantization pipeline and inference throughput",
        "desc": [
            "Recorded INT8 vs FP16 latency and throughput benchmarks",
            "Optimized memory footprint for ONNX / TensorRT runtime execution",
            "Synced edge inference telemetry logs",
        ],
        "module": "Edge AI Inference Engine",
        "details": {
            "metric": "latency_ms",
            "target": "ARM Cortex-M / Raspberry Pi",
            "framework": "ONNX/TFLite",
        },
    },
    {
        "scope": "agents",
        "type": "refactor",
        "title": "streamline async memory buffer and context pruning",
        "desc": [
            "Refined sliding context window management for autonomous agents",
            "Reduced redundant state serialization overhead in agent loop",
            "Updated agentic coordination telemetry",
        ],
        "module": "Agentic System Core",
        "details": {
            "metric": "token_latency",
            "pattern": "Event-Driven Coordinator",
            "status": "stable",
        },
    },
    {
        "scope": "embedded",
        "type": "fix",
        "title": "refine circular ring buffer boundary checks and DMA sync",
        "desc": [
            "Hardened edge sensor stream ingestion routines against packet drops",
            "Validated thread-safe DMA buffer exchange mechanism",
            "Updated hardware communication diagnostics",
        ],
        "module": "Embedded Sensor Layer",
        "details": {
            "hardware": "ESP32 / Microcontrollers",
            "protocol": "SPI / I2C / UART",
            "throughput_kbps": 1250,
        },
    },
    {
        "scope": "telemetry",
        "type": "feat",
        "title": "record telemetry event processing and latency histograms",
        "desc": [
            "Aggregated real-time system metrics across active execution nodes",
            "Updated sliding window percentiles (p50, p95, p99)",
            "Persisted node telemetry snapshot",
        ],
        "module": "Distributed Metrics Aggregator",
        "details": {
            "p50_ms": 12.4,
            "p95_ms": 28.1,
            "p99_ms": 41.6,
            "active_nodes": 8,
        },
    },
    {
        "scope": "architecture",
        "type": "docs",
        "title": "document decentralized edge node failover and topology specs",
        "desc": [
            "Updated network topology graph for autonomous edge clusters",
            "Defined node self-healing protocol during intermittent connectivity",
            "Refreshed architectural decision record (ADR)",
        ],
        "module": "System Architecture",
        "details": {
            "spec_version": "v2.4",
            "topology": "Peer-to-Peer Mesh",
            "consensus": "Raft-Light",
        },
    },
    {
        "scope": "vision",
        "type": "perf",
        "title": "benchmark spatial feature extraction and bounding-box pruning",
        "desc": [
            "Evaluated low-latency NMS (Non-Maximum Suppression) kernels",
            "Measured frame-time variance on resource-constrained devices",
            "Recorded vision pipeline performance matrix",
        ],
        "module": "Edge Vision Pipeline",
        "details": {"fps": 42.8, "resolution": "640x480", "precision": "FP16"},
    },
    {
        "scope": "runtime",
        "type": "feat",
        "title": "update edge node heartbeat telemetry and health status",
        "desc": [
            "Collected cluster node availability and memory utilization rates",
            "Validated automated failover routines for detached sensors",
            "Synced daily operational health ledger",
        ],
        "module": "Cluster Health Monitor",
        "details": {
            "cluster_status": "healthy",
            "memory_usage_pct": 34.2,
            "uptime_hours": 312,
        },
    },
    {
        "scope": "algorithms",
        "type": "refactor",
        "title": "modularize tensor transformation and SIMD acceleration kernels",
        "desc": [
            "Implemented vectorized dot-product routines for matrix multiplication",
            "Reduced cache misses by aligning memory strides in hot loops",
            "Updated numerical computation benchmarks",
        ],
        "module": "SIMD Acceleration Lib",
        "details": {
            "instruction_set": "NEON / AVX2",
            "speedup_factor": "2.8x",
            "cache_hit_rate": "98.2%",
        },
    },
]


def check_user_activity(username: str, token: str = "") -> bool:
    """Checks if the user has already committed or pushed today in UTC."""
    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Checking commit activity for {username} on {today_utc} (UTC)...")

    headers = {"User-Agent": "Daily-Contribution-Bot"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"https://api.github.com/users/{username}/events"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            events = json.loads(resp.read().decode("utf-8"))
            pushes_today = [
                e
                for e in events
                if e.get("type") == "PushEvent"
                and e.get("created_at", "").startswith(today_utc)
            ]
            if pushes_today:
                print(
                    f"Found {len(pushes_today)} push event(s) today by {username}."
                )
                return True
            print(f"No push events found for {username} today.")
            return False
    except Exception as e:
        print(f"Warning: Failed to fetch events from GitHub API ({e}).")
        print("Proceeding with safety commit to prevent streak disruption.")
        return False


def generate_engineering_update():
    """Selects a topic and updates the engineering telemetry log."""
    os.makedirs("data", exist_ok=True)
    os.makedirs("generated", exist_ok=True)

    history = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    # Pick a topic that wasn't used in the immediate previous update
    last_scope = history[-1].get("scope") if history else None
    available_topics = [t for t in TOPICS if t["scope"] != last_scope]
    if not available_topics:
        available_topics = TOPICS

    chosen = random.choice(available_topics)
    now_utc = datetime.now(timezone.utc)
    timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    date_str = now_utc.strftime("%Y-%m-%d")

    entry = {
        "timestamp": timestamp_str,
        "date": date_str,
        "scope": chosen["scope"],
        "type": chosen["type"],
        "module": chosen["module"],
        "title": chosen["title"],
        "highlights": chosen["desc"],
        "telemetry": chosen["details"],
    }

    history.append(entry)
    # Keep last 50 entries
    if len(history) > 50:
        history = history[-50:]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    with open(LAST_UPDATED_FILE, "w", encoding="utf-8") as f:
        f.write(f"Last updated: {timestamp_str}\n")

    # Generate commit message and description
    commit_msg = f"{chosen['type']}({chosen['scope']}): {chosen['title']}"
    commit_body = "\n".join(f"- {line}" for line in chosen["desc"])
    full_commit_message = f"{commit_msg}\n\n{commit_body}\n"

    commit_msg_file = os.path.join("generated", ".commit_msg.tmp")
    with open(commit_msg_file, "w", encoding="utf-8") as f:
        f.write(full_commit_message)

    return full_commit_message


def main():
    force = os.environ.get("FORCE_RUN", "false").lower() == "true"
    token = os.environ.get("GITHUB_TOKEN", "")
    username = "Pranshmish"

    github_output = os.environ.get("GITHUB_OUTPUT")

    if not force:
        has_committed = check_user_activity(username, token)
        if has_committed:
            print("User has already committed today. Skipping auto-commit.")
            if github_output:
                with open(github_output, "a", encoding="utf-8") as f:
                    f.write("should_commit=false\n")
            return

    print("Generating professional engineering update and commit...")
    commit_message = generate_engineering_update()

    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write("should_commit=true\n")
            # Write multiline commit message to GITHUB_OUTPUT safely
            f.write("commit_msg<<EOF\n")
            f.write(f"{commit_message}\n")
            f.write("EOF\n")
    else:
        print("Generated Commit Message:\n")
        print(commit_message)


if __name__ == "__main__":
    main()
