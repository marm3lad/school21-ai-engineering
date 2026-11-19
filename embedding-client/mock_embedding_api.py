from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

attempts = {}
FAIL_RATE = 0.3

@app.route("/embed", methods=["POST"])
def embed():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "нужен text"}), 400
    attempts[text] = attempts.get(text, 0) + 1
    if text == "сбой500" and attempts.get(text) <= 2:
        return jsonify({"error": "внутренняя ошибка"}), 500
    elif text == "сбой429" and attempts.get(text) <= 2:
        return jsonify({"error": "слишком много запросов"}), 429
    elif text == "сбой503" and attempts.get(text) <= 2:
        return jsonify({"error": "сервис не доступен"}), 503
    elif text == "случайно" and random.random() < FAIL_RATE:
        return jsonify({"error": "внутренняя ошибка"}), 500
    if text == "медленно" and attempts.get(text) <= 2:
        time.sleep(5)
    numbers = []
    for _ in range(128):
        numbers.append(random.random())
    return jsonify({"embedding": numbers})

if __name__ == "__main__":
    app.run(port=5000)