import sqlite3
import re
import time
import os
from urllib.parse import unquote
from datetime import datetime

LOG_FILE = "/home/kali/advanced-soc/logs/access.log"

DB_PATH = "/home/kali/advanced-soc/database/soc.db"

patterns = {

    "SQL Injection": {
        "pattern": r"(union(\s+all)?\s+select|or\s+1=1|drop\s+table|insert\s+into)",
        "severity": "CRITICAL",
        "mitre": "T1190"
    },

    "XSS Attack": {
        "pattern": r"(<script>|javascript:|alert\()",
        "severity": "HIGH",
        "mitre": "T1059"
    },

    "Command Injection": {
        "pattern": r"(cmd=|whoami|cat|ls|bash|nc )",
        "severity": "CRITICAL",
        "mitre": "T1059.004"
    },

    "Directory Traversal": {
        "pattern": r"(\.\./|etc/passwd)",
        "severity": "CRITICAL",
        "mitre": "T1083"
    }
}

def save_incident(data):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO incidents
    (
        timestamp,
        ip,
        attack_type,
        severity,
        mitre,
        endpoint,
        status_code,
        raw_log
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["ip"],
        data["attack_type"],
        data["severity"],
        data["mitre"],
        data["endpoint"],
        data["status_code"],
        data["raw_log"]
    ))

    conn.commit()
    conn.close()


def extract_ip(line):

    try:
        return line.split()[0]
    except:
        return "Unknown"


def extract_endpoint(line):

    match = re.search(r'\"GET (.*?) HTTP', line)

    if match:
        return match.group(1)

    return "Unknown"


def extract_status(line):

    match = re.search(r'HTTP\/1\.[01]" (\d+)', line)

    if match:
        return match.group(1)

    return "000"


print("\n🛡️ ADVANCED SOC DETECTOR STARTED")
print("=" * 60)

if not os.path.exists(LOG_FILE):

    print("❌ Log file missing")
    exit()

with open(LOG_FILE, "r") as file:

    file.seek(0, 2)

    while True:

        line = file.readline()

        if not line:
            time.sleep(1)
            continue

        decoded = unquote(line)

        print("📥", decoded.strip())

        for attack_name, attack_data in patterns.items():

            if re.search(attack_data["pattern"], decoded, re.IGNORECASE):

                incident = {

                    "timestamp": str(datetime.now()),

                    "ip": extract_ip(decoded),

                    "attack_type": attack_name,

                    "severity": attack_data["severity"],

                    "mitre": attack_data["mitre"],

                    "endpoint": extract_endpoint(decoded),

                    "status_code": extract_status(decoded),

                    "raw_log": decoded.strip()
                }

                save_incident(incident)

                print("\n🚨 ATTACK DETECTED")
                print("IP:", incident["ip"])
                print("Type:", incident["attack_type"])
                print("Severity:", incident["severity"])
                print("MITRE:", incident["mitre"])
                print("=" * 60)

                break
