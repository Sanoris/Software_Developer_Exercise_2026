from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

patient_details = pd.read_csv("./data/fake_patient_details.csv")
patient_diagnosis = pd.read_csv("./data/fake_patient_diagnosis.csv")
patient_genes = pd.read_csv("./data/fake_patient_genes.csv")

df = pd.merge(patient_details, patient_diagnosis, on="patient_id")
df = pd.merge(df, patient_genes, on="patient_id")

@app.route("/")
def home():
    return df.to_html()


if __name__ == "__main__":
    app.run(debug=True, port=5000)