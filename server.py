from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Initialize OpenAI client, reading API key from env variable for safety
openai.api_key = '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'
# 🔐 Direct API key set (not recommended for production)

app = Flask(__name__)
CORS(app)

@app.route('/verse', methods=['POST'])
def get_verse():
    try:
        # Check if request contains JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        topic = data.get('topic', '').strip()

        if not topic:
            return jsonify({"error": "Missing or empty 'topic' in request body"}), 400

        print(f"[🔍] Topic received: {topic}")

        prompt = (
            f"Give only one Bible verse reference (book, chapter, and verse) from the NKJV about the topic '{topic}'. "
            "Do not quote the verse. Do not explain. Only return the reference."
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        reference = response.choices[0].message.content.strip()
        print(f"[✅] Verse reference: {reference}")
        return jsonify({"verse": reference})

    except Exception as e:
        print(f"[🔥 ERROR] {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
