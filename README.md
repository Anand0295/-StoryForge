# 🔥 StoryForge
> **Transform your imagination into epic novels with AI-powered storytelling**

StoryForge is an advanced AI story generator that creates full-length, coherent novels from simple prompts. Whether you're a writer seeking inspiration, a game master crafting campaigns, or simply someone who loves great stories, StoryForge brings your ideas to life with remarkable depth and creativity.

## ✨ Features
- 📚 **Full-Length Novels** - Generate complete stories with multiple chapters, character arcs, and satisfying conclusions
- 🎭 **Multi-Genre Support** - Fantasy, sci-fi, mystery, romance, adventure, and hybrid genres
- 🏠 **100% Local Processing** - Your stories remain private on your machine
- 📄 **PDF Export** - Professional formatting for easy reading and sharing
- 🌐 **Web Interface** - Clean, intuitive Gradio-based UI accessible via browser
- ⚡ **Smart Generation** - Context-aware storytelling that maintains character consistency
- 🔧 **Highly Customizable** - Extensive configuration options for advanced users

## 📦 Installation

### Prerequisites
- **Python**: 3.8+
- **RAM**: 8GB minimum, 16GB recommended
- **GPU** (Optional but recommended): NVIDIA RTX series or Apple Silicon
- **Model**: `llama3.1:latest` (5GB download)
- **Storage**: 10GB+ for multiple models

### Performance Guide
| Hardware | Model | Generation Time | Quality |
|----------|-------|-----------------|----------|
| CPU Only | llama3.2 | 5-10 min | Good |
| RTX 3060+ | llama3.1 | 2-5 min | Excellent |
| Apple M1+ | llama3.1 | 3-7 min | Excellent |

## 🎯 Usage

### Command Line Interface
```bash
# Basic usage with default settings
python Write.py -Prompt "Your story idea here"

# Advanced usage with custom models
python Write.py -Prompt prompts/fantasy.txt \
  -InitialOutlineModel "ollama://llama3.1:latest" \
  -ChapterModel "ollama://llama3.1:latest"
```

## 🖥️ Frontend Creation

### Overview
Create a simple web interface for StoryForge to make story generation more accessible and user-friendly.

### Recommended Stack

#### Option 1: React Frontend
- **Framework**: React.js with Vite
- **UI Library**: Material-UI or Tailwind CSS
- **State Management**: React Context or Redux
- **API Communication**: Axios or Fetch API

#### Option 2: Flask Minimal Interface
- **Framework**: Flask with Jinja2 templates
- **Styling**: Bootstrap or plain CSS
- **Backend Integration**: Direct Python integration

### Setup Steps

#### React Frontend Setup
```bash
# Create new React project
npm create vite@latest storyforge-frontend -- --template react
cd storyforge-frontend
npm install

# Install dependencies
npm install axios
```

#### Flask Setup
```bash
# Install Flask
pip install flask flask-cors

# Create app structure
mkdir storyforge_web
cd storyforge_web
touch app.py
mkdir templates static
```

### Example Code Snippets

#### React Component Example
```javascript
import { useState } from 'react';
import axios from 'axios';

function StoryGenerator() {
  const [prompt, setPrompt] = useState('');
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);

  const generateStory = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/generate', {
        prompt: prompt,
        model: 'ollama://llama3.1:latest'
      });
      setStory(response.data.story);
    } catch (error) {
      console.error('Error generating story:', error);
    }
    setLoading(false);
  };

  return (
    <div className="story-generator">
      <h1>StoryForge</h1>
      <textarea 
        value={prompt} 
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your story idea..."
      />
      <button onClick={generateStory} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Story'}
      </button>
      {story && <div className="story-output">{story}</div>}
    </div>
  );
}

export default StoryGenerator;
```

#### Flask Backend Wrapper
```python
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.json
    prompt = data.get('prompt', '')
    model = data.get('model', 'ollama://llama3.1:latest')
    
    # Call the Write.py CLI
    cmd = [
        'python', 'Write.py',
        '-Prompt', prompt,
        '-InitialOutlineModel', model
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return jsonify({
            'success': True,
            'story': result.stdout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

#### Simple HTML Template (Flask)
```html
<!DOCTYPE html>
<html>
<head>
    <title>StoryForge</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 150px; margin: 10px 0; padding: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px; }
        button:hover { background: #0056b3; }
        .story-output { margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 5px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>🎭 StoryForge</h1>
    <textarea id="prompt" placeholder="Enter your story idea..."></textarea>
    <button onclick="generateStory()">Generate Story</button>
    <div id="output" class="story-output" style="display:none;"></div>
    
    <script>
        async function generateStory() {
            const prompt = document.getElementById('prompt').value;
            const output = document.getElementById('output');
            output.style.display = 'block';
            output.textContent = 'Generating story...';
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });
            
            const data = await response.json();
            output.textContent = data.story;
        }
    </script>
</body>
</html>
```

### Running the Frontend

#### React Development Server
```bash
npm run dev
# Access at http://localhost:5173
```

#### Flask Server
```bash
python app.py
# Access at http://localhost:5000
```

### Integration Notes
- Ensure the backend CLI (`Write.py`) is accessible from your frontend server
- Configure CORS properly if running React and Flask separately
- Consider adding authentication for production deployments
- Implement proper error handling and loading states
- Add file upload support for prompt files
