from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD", # <-- Update this
    "host": "127.0.0.1",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """Endpoint for: Fetching anomaly logs"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM "anomaly_logs" ORDER BY timestamp DESC LIMIT 100;')
    logs = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(logs)

@app.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient_history(patient_id):
    """Endpoint for: Patient-wise history"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM "anomaly_logs" WHERE patient_id_number = %s ORDER BY timestamp DESC;', (patient_id,))
    history = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(history)

@app.route('/api/baselines', methods=['GET'])
def get_baselines():
    """Endpoint for: Baseline vitals"""
    # Simulated baseline data as per medical standards
    baselines = {
        "heart_rate": {"min": 60, "max": 100, "unit": "BPM"},
        "spo2": {"min": 95, "max": 100, "unit": "%"},
        "temp": {"min": 36.5, "max": 37.5, "unit": "°C"}
    }
    return jsonify(baselines)

if __name__ == '__main__':
    app.run(port=5000, debug=True)