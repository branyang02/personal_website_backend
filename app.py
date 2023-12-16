from flask import Flask, request, jsonify
from util import get_word_details
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    sample_data = {"key": "value", "hello": "world"}
    return jsonify(sample_data)

@app.route('/api/word-details/<word>', methods=['GET'])
def word_details(word):
    if not word:
        return jsonify({"error": "No word provided"}), 400

    try:
        word_details = get_word_details(word)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(word_details)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
