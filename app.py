from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in Render secrets

@app.route("/")
def index():
    return "Unify API is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Example prompt for OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract personal information from the following text:"},
            {"role": "user", "content": text}
        ]
    )

    return jsonify(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
