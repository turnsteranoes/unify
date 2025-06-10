from flask import Flask, request, jsonify, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in Render secrets

# Serve a simple UI page
@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Unify Analyzer</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    textarea { width: 100%; height: 150px; font-size: 1rem; }
    #notes { margin-top: 20px; padding: 1rem; border: 1px solid #ccc; white-space: pre-wrap; background: #f9f9f9; }
    button { margin-top: 10px; padding: 0.5rem 1rem; font-size: 1rem; }
  </style>
</head>
<body>
  <h1>Unify Personal Info Extractor</h1>
  <textarea id="inputText" placeholder="Paste chat text here..."></textarea><br/>
  <button onclick="analyze()">Extract Info</button>

  <h2>Extracted Notes:</h2>
  <div id="notes">Results will appear here...</div>

  <script>
    async function analyze() {
      const text = document.getElementById("inputText").value;
      if (!text.trim()) {
        alert("Please paste some text first.");
        return;
      }
      document.getElementById("notes").textContent = "Analyzing...";

      try {
        const response = await fetch("/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });
        if (!response.ok) {
          const error = await response.json();
          document.getElementById("notes").textContent = "Error: " + (error.error || "Unknown error");
          return;
        }
        const data = await response.json();
        document.getElementById("notes").textContent = data;
      } catch (err) {
        document.getElementById("notes").textContent = "Fetch error: " + err.message;
      }
    }
  </script>
</body>
</html>
    """)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Prompt OpenAI with an enhanced system prompt for better extraction
    system_prompt = """
You are an assistant that extracts detailed personal information from text.
Extract and list clearly:
- Name
- Job
- Activities
- Appearance
- Hobbies
- Relationship status
- Kids (how many and names)
- Brothers or sisters
- Parents or family info
- Health problems
- Sexual preferences
- What he/she likes to do in free time
- Plans for today or future

Return the information in a neat, bullet-point list.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )

    return jsonify(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
