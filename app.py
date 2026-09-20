from flask import Flask, request, jsonify, send_from_directory
from client import ask_agent

app = Flask(__name__)

@app.route("/")
def home():
    # Serves the HTML page below
    return send_from_directory(".", "index.html")

@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    user_text = data.get("text", "")

    # ---- Do whatever processing you want here ----
    result = ask_agent(user_text)
    # ------------------------------------------------

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=False, port=5000)