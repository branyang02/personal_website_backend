from flask import Flask, request, jsonify, Response
from util import get_word_details, get_audio
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

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    print("request", request)
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = get_audio(text)
        return Response(response.content, mimetype="audio/mpeg")  # adjust mimetype based on the format

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
