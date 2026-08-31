from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os
import sqlite3

def getConnection():
    conn = sqlite3.connect('./data/patients.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__, static_folder='./frontend/dist', static_url_path='')

#initial db setup - not needed on subsequent runs
'''conn = getConnection()
patient_details = pd.read_csv("./data/fake_patient_details.csv").to_sql('patient', conn)
patient_diagnosis = pd.read_csv("./data/fake_patient_diagnosis.csv").to_sql('diagnosis', conn)
patient_genes = pd.read_csv("./data/fake_patient_genes.csv").to_sql('genes', conn)
conn.commit()'''

@app.route("/api/patients", methods=["GET"])
def get_patients():
    first_name = request.args.get("first_name", "").strip().lower()
    last_name = request.args.get("last_name", "").strip().lower()
    state = request.args.get("state", "").strip().lower()
    diagnosis = request.args.get("diagnosis", "").strip().lower()
    gene = request.args.get("gene", "").strip().lower()

    query = """
        SELECT 
            patient.*,
            GROUP_CONCAT(DISTINCT genes.gene) as gene,
            GROUP_CONCAT(DISTINCT diagnosis.diagnosis) as diagnosis
        FROM patient
        LEFT JOIN diagnosis on diagnosis.patient_id = patient.patient_id
        LEFT JOIN genes on genes.patient_id = patient.patient_id
        WHERE patient.first_name LIKE ?
            AND patient.last_name LIKE ?
            AND patient.state LIKE ?
            AND (
                ? = ''
                OR patient.patient_id in (SELECT diagnosis.patient_id FROM diagnosis WHERE diagnosis.diagnosis LIKE ?)
            )
            AND (
                ? = ''
                OR patient.patient_id in (SELECT genes.patient_id FROM genes WHERE genes.gene LIKE ?)
            )
        GROUP BY patient.patient_id
    """
    params = (
        f"%{first_name}%",
        f"%{last_name}%",
        f"%{state}%",
        diagnosis,
        f"%{diagnosis}%",
        gene,
        f"%{gene}%"
    )
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]

    return jsonify(records)

# Serve static files and handle client-side routing fallback
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Return specific static file if it exists, otherwise fall back to index.html
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)