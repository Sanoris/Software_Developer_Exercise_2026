from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__, static_folder='static', static_url_path='/static')

patient_details = pd.read_csv("./data/fake_patient_details.csv")
patient_diagnosis = pd.read_csv("./data/fake_patient_diagnosis.csv")
patient_genes = pd.read_csv("./data/fake_patient_genes.csv")

df = pd.merge(patient_details, patient_diagnosis, on="patient_id")
df = pd.merge(df, patient_genes, on="patient_id")

@app.route("/")
def home():
    return app.send_static_file("home.html")

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

if __name__ == "__main__":
    app.run(debug=True, port=5000)