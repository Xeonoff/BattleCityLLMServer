import os
from flask import Flask, request, jsonify
from flask_cors import CORS  
from openai import OpenAI

app = Flask(__name__)
CORS(app)  

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_API_KEY"),
)

@app.route('/generate', methods=['POST', 'GET'])
def generate_text():
    try:
        if request.method == 'GET':
            return jsonify({"message": "Сервер работает! Используйте POST запрос с промптом."})

        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        print(f"Received prompt: {prompt}") 

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:cerebras",
            messages=[{"role": "user", "content": prompt}],
        )

        result = completion.choices[0].message.content
        return jsonify({"response": result})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "Server is running", "endpoints": {"/generate": "POST with JSON {prompt: 'your text'}"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)