from flask import Flask, jsonify, request
from ai.predictor import TradingAI


app = Flask(__name__)

bot = TradingAI()


@app.route("/")
def home():
    return {
        "status":"SAI ONLINE",
        "version":"V2"
    }


@app.route("/predict", methods=["POST"])
def predict():

    data=request.json

    result=bot.predict(data)

    return jsonify(result)


if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )