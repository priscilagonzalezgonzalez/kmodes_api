from flask import Flask, jsonify, request
from conexion import get_prediction, train_model

app = Flask(__name__)
# Initialize Kmodes
train_model()

@app.route("/api/v1/predictions/<int:id>", methods=["GET"])
def predict(id):
    return jsonify(get_prediction(id))


app.run(debug=True)