from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv('OPENROUTER_API_KEY')
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    try:
        user_prompt = request.json.get('prompt', '')
        
        if not user_prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        if not API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
        
        # Prepare the API request
        headers = {
            'Authorization': f'Bearer {API_KEY}' if API_KEY else '',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'Hello AI App'
        }
        
        payload = {
            'model': 'deepseek/deepseek-chat-v3.1:free',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant. Provide concise and helpful responses.'},
                {'role': 'user', 'content': user_prompt}
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        # Send request to OpenAI API
        response = requests.post(API_URL, json=payload, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            ai_response = response_data['choices'][0]['message']['content']
            return jsonify({'response': ai_response})
        else:
            error_msg = response_data.get('error', {}).get('message', 'Unknown error')
            return jsonify({'error': error_msg}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)