import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
PPLX_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    if not question:
        return jsonify({'answer': 'Please ask a question.'})

    try:
        headers = {
            'Authorization': f'Bearer {PPLX_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "model": "sonar-small-online",
            "messages": [{"role": "user", "content": question}]
        }
        r = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        answer = data['choices'][0]['message']['content']
    except Exception as e:
        answer = f"Error: {str(e)}"

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
