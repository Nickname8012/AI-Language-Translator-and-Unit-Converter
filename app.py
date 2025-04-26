from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from googletrans import Translator
import os

app = Flask(__name__)

# Configure Google AI
GOOGLE_API_KEY = "AIzaSyC2OVP_fIV24tivyaGzrQyPV9cGx1fz5XE"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize translator
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translator')
def translator_page():
    return render_template('translator.html')

@app.route('/calculator')
def calculator_page():
    return render_template('calculator.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'auto')
    target_lang = data.get('target_lang', 'en')
    
    try:
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        return jsonify({
            'success': True,
            'translated_text': translation.text
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content([{'role': 'user', 'parts': [user_message]}])
        text = ""
        if hasattr(response, "text"):
            text = response.text
        elif hasattr(response, "candidates") and response.candidates:
            text = response.candidates[0].content.parts[0].text
        return jsonify({
            'success': True,
            'response': text
        })
    except Exception as e:
        print("Gemini API error:", e)  # Log the error to the console
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # <- dynamic port for deployment
    app.run(host='0.0.0.0', port=port, debug=True)  # <- 0.0.0.0 binding
