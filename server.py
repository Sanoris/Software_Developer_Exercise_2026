from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__, static_folder='./frontend/dist', static_url_path='')

patient_details = pd.read_csv("./data/fake_patient_details.csv")
patient_diagnosis = pd.read_csv("./data/fake_patient_diagnosis.csv")
patient_genes = pd.read_csv("./data/fake_patient_genes.csv")

df = pd.merge(patient_details, patient_diagnosis, on="patient_id")
df = pd.merge(df, patient_genes, on="patient_id")

@app.route("/api/patients", methods=["GET"])
def get_patients():
    first_name = request.args.get("first_name", "").strip().lower()
    last_name = request.args.get("last_name", "").strip().lower()
    state = request.args.get("state", "").strip().lower()
    diagnosis = request.args.get("diagnosis", "").strip().lower()
    gene = request.args.get("gene", "").strip().lower()

    filtered_df = df[
        (df["first_name"].str.lower().str.contains(first_name)) &
        (df["last_name"].str.lower().str.contains(last_name)) &
        (df["state"].str.lower().str.contains(state)) &
        (df["diagnosis"].str.lower().str.contains(diagnosis)) &
        (df["gene"].str.lower().str.contains(gene))
    ]

    return jsonify(filtered_df.to_dict(orient="records"))

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