from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in Render secrets

@app.route("/")
def index():
    return "Unify AI Extractor is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
Extract the following information from the text below and return it as a JSON object with these fields:
name, job, location, appearance, hobbies, activities, relationship, kids, siblings, parents, sexual_preferences, health, plans, vehicles.

Text:
\"\"\"{text}\"\"\"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a personal information extractor. Always respond with a JSON object."},
            {"role": "user", "content": prompt}
        ]
    )

    # Try parsing as JSON
    try:
        import json
        parsed = json.loads(response["choices"][0]["message"]["content"])
        return jsonify(parsed)
    except Exception as e:
        return jsonify({"error": "Invalid JSON from OpenAI", "raw": response["choices"][0]["message"]["content"]}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
