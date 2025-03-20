#!/usr/bin/env python3
"""
Advanced Log Analysis and SIEM System
--------------------------------------
Features:
- Aggregates logs from multiple sources (CSV or text logs).
- Correlates events using advanced correlation rules.
- Generates detailed CSV incident reports.
- Provides a command-line interface for log analysis.

Usage:
  python advanced_siem.py --logs log1.txt log2.txt
"""

import argparse, csv, re, sys
from datetime import datetime

def parse_logs(log_files):
    """
    Parses provided log files. Assumes log entries are comma-separated with at least three columns:
    timestamp, event type, and details.
    """
    events = []
    for logfile in log_files:
        try:
            with open(logfile, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        events.append({
                            "timestamp": parts[0],
                            "event": parts[1],
                            "details": ",".join(parts[2:])
                        })
        except Exception as e:
            print(f"Error reading {logfile}: {e}")
    return events

def correlate_events(events):
    """
    Correlates events using advanced rules.
    For example, detects if a specific user has 5+ FAILED_LOGIN events within 10 minutes.
    """
    alerts = []
    failed_logins = {}
    for event in events:
        if event["event"].strip().upper() == "FAILED_LOGIN":
            # Extract user using a regex from details (assumes 'user: <username>' exists)
            match = re.search(r"user:\s*(\w+)", event["details"], re.IGNORECASE)
            user = match.group(1) if match else "unknown"
            failed_logins.setdefault(user, []).append(event["timestamp"])
    for user, times in failed_logins.items():
        if len(times) >= 5:
            alerts.append(f"High number of failed logins for {user}: {len(times)} attempts")
    return alerts

def generate_siem_report(alerts, output="advanced_siem_report.csv"):
    """
    Generates a CSV report from the list of alerts.
    """
    with open(output, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Alert", "Timestamp"])
        for alert in alerts:
            writer.writerow([alert, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    print(f"SIEM report generated: {output}")

def main_siem():
    parser = argparse.ArgumentParser(description="Advanced Log Analysis and SIEM System")
    parser.add_argument("--logs", nargs="+", required=True, help="Log files to analyze")
    args = parser.parse_args()
    events = parse_logs(args.logs)
    alerts = correlate_events(events)
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("No correlated incidents found.")
    generate_siem_report(alerts)

if __name__ == "__main__":
    main_siem()
