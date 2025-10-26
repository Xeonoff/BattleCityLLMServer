import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_API_KEY"), 
)

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=[{"role": "user", "content": prompt}],
        )

        result = completion.choices[0].message.content
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "Server is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))