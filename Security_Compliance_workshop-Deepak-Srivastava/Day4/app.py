from flask import Flask, request
import os

app = Flask(__name__)

# ❌ Hardcoded secret
SECRET_KEY = "supersecret123"

@app.route("/")
def hello():
    user = request.args.get("user", "World")
    # ❌ Insecure string concatenation (potential XSS)
    return f"Hello {user}"

@app.route("/insecure")
def insecure():
    user_input = request.args.get("data")
    return str(eval(user_input))  # vulnerable to code injection

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
