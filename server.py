from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)