from flask import Flask, jsonify, request
from flask_cors import CORS
from conexion import get_prediction, train_model


def start_app():
    app = Flask(__name__)
    CORS(app)
    # Initialize Kmodes
    train_model()

    @app.route("/api/v1/predictions/<int:id>", methods=["GET"])
    def predict(id):
        return jsonify(get_prediction(id))
    
    return app

if __name__ == "__main__":
    app =  start_app()
    app.run()
