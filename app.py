from flask import Flask, request, jsonify, Response
from util import get_word_details, get_audio, run_c_code_sync
from flask_cors import CORS
import os
import subprocess
import base64


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/api/data", methods=["GET"])
def get_data():
    sample_data = {"key": "value", "hello": "world"}
    return jsonify(sample_data)


@app.route("/api/word-details/<word>", methods=["GET"])
def word_details(word):
    if not word:
        return jsonify({"error": "No word provided"}), 400

    try:
        word_details = get_word_details(word)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(word_details)


@app.route("/api/text-to-speech", methods=["POST"])
def text_to_speech():
    print("request", request)
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = get_audio(text)
        return Response(
            response.content, mimetype="audio/mpeg"
        )  # adjust mimetype based on the format

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/run-c-code", methods=["POST"])
def run_c_code():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data["code"]

    try:
        output = run_c_code_sync(code)
    except Exception as e:
        output = str(e)
    finally:
        return jsonify({"output": output})


@app.route("/api/run-python-code", methods=["POST"])
def run_python_code():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data["code"]

    # List of potentially dangerous modules or functions
    blocked_keywords = {
        "open",
        "file",
        "exec",
        "eval",
        "subprocess",
        "os.system",
        "import os",
        "__import__",
        "sys",
    }

    # Check for dangerous keywords
    if any(keyword in code for keyword in blocked_keywords):
        print("Operation not allowed")
        return jsonify({"output": "Error: Operation not allowed"})

    pre_code = """
import matplotlib.pyplot as plt
import numpy as np
def get_image(fig):
    filename="image.png"
    fig.savefig(filename)
"""
    print(pre_code + code)
    encoded_string = ""
    try:
        result = subprocess.run(
            ["python3", "-c", pre_code + code],
            text=True,
            capture_output=True,
            check=True,
        )
        output = result.stdout
        # Check if the image file exists and encode it
        if os.path.exists("image.png"):
            with open("image.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            os.remove("image.png")
    except subprocess.CalledProcessError as e:
        output = e.stderr
    finally:
        return jsonify({"output": output, "image": encoded_string})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1234))
    app.run(host="0.0.0.0", port=port)
