from flask import Flask, render_template, request, jsonify
import pandas as pd
from model import run_segmentation

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["file"]

    rfm_data, summary = run_segmentation(file)

    return jsonify({
        "data": rfm_data,
        "summary": summary
    })


if __name__ == "__main__":
    app.run(debug=True)