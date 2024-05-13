import base64
import os
import subprocess
from flask import jsonify

from util import run_c_code_sync, run_any_code_sync


def run_code(code, language):
    if language == "python":
        return run_python(code)
    elif language == "c":
        return run_c(code)
    else:
        return run_any(code, language)


def run_python(code):
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


def run_c(code):
    try:
        output = run_c_code_sync(code)
    except Exception as e:
        output = str(e)
    finally:
        return jsonify({"output": output})


def run_any(code, language):
    try:
        output = run_any_code_sync(code, language)
    except Exception as e:
        output = str(e)
    finally:
        return jsonify({"output": output})
