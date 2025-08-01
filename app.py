from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
from model_integration import ModelIntegration

app = Flask(__name__)

# Initialize the model integration with Hugging Face Transformers
# By default, we use mock mode for GitHub Codespaces to avoid loading the large model
# Set use_mock=False to use the actual UnfilteredAI/NSFW-3B model
model = ModelIntegration(model_name="UnfilteredAI/NSFW-3B", use_mock=True)  # Mock mode for GitHub Codespaces

# Serve the static HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API endpoint for generating stories
@app.route('/api/generate', methods=['POST'])
def generate_story():
    data = request.json
    prompt = data.get('prompt', '')
    genre = data.get('genre', 'romance')
    length = data.get('length', 'medium')
    temperature = data.get('temperature', 0.7)
    
    # Generate the story using the model integration
    story = model.generate_story(prompt, genre, length, temperature)
    
    return jsonify({
        'story': story,
        'status': 'success'
    })

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': not model.mock_mode
    })

if __name__ == '__main__':
    # Get port from environment variable for Codespaces compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)