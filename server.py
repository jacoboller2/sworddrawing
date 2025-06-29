from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_file('index.html')


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

        response = openai.ChatCompletion.create(
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
