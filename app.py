from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "/home/kali/advanced-soc/database/soc.db"


# ---------------- DB HELPER ----------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- MAIN DASHBOARD ----------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ---------------- INCIDENTS API ----------------
@app.route("/api/incidents")
def incidents():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


# ---------------- STATS API ----------------
@app.route("/api/stats")
def stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM incidents")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM incidents WHERE severity='CRITICAL'")
    critical = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM incidents WHERE severity='HIGH'")
    high = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM incidents WHERE severity='MEDIUM'")
    medium = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(DISTINCT ip) as total FROM incidents")
    ips = cursor.fetchone()["total"]

    conn.close()

    return jsonify({
        "total": total,
        "critical": critical,
        "high": high,
        "medium": medium,
        "ips": ips
    })


# ---------------- CHART API ----------------
@app.route("/api/chart")
def chart():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT attack_type FROM incidents")
    data = cursor.fetchall()
    conn.close()

    result = {}

    for row in data:
        attack = row["attack_type"]
        result[attack] = result.get(attack, 0) + 1

    return jsonify(result)


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    print("🛡️ Advanced SOC Dashboard Running")
    print("🌐 http://127.0.0.1:5000")

    app.run(host="0.0.0.0", port=5000, debug=True)
