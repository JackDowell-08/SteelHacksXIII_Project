from flask import Flask, request, jsonify, send_from_directory

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
    result = user_text.upper()  # example: just uppercase it
    # ------------------------------------------------

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)