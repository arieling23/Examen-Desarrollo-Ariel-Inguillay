from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from transformers import pipeline # type: ignore

app = Flask(__name__)
CORS(app)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = ["deportes", "política", "religión", "cine"]
history = []

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    code = data.get("code")
    value = data.get("value")

    if not isinstance(code, int) or not isinstance(value, str):
        return jsonify({"error"}), 400

    result = classifier(value, labels)
    if result['scores'][0] < 0.5:
        label = "No puedo generar una etiqueta, porque solo tengo el entrenamiento en deportes, política, religión y cine"
    else:
        label = result['labels'][0]

    response = {"code": code, "label": label}
    history.append(response)
    return jsonify(response)

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)

if __name__ == '__main__':
    app.run(port=8008)
