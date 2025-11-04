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
| Hardware     | Model         | Generation Time | Quality   |
|-------------|--------------|----------------|-----------|
| CPU Only    | llama3.2     | 5-10 min       | Good      |
| RTX 3060+   | llama3.1     | 2-5 min        | Excellent |
| Apple M1+   | llama3.1     | 3-7 min        | Excellent |

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
Create new React project
```bash
npm create vite@latest storyforge-frontend -- --template react
cd storyforge-frontend
npm install
```
Install dependencies
```bash
npm install axios
```
#### Flask Setup
Install Flask
```bash
pip install flask flask-cors
```
Create app structure
```bash
mkdir storyforge_web
cd storyforge_web
touch app.py
mkdir templates static
```

### Example Code Snippets
#### React Component Example
```javascript
import React, { useState } from 'react';
import axios from 'axios';
function StoryGenerator() {
  const [prompt, setPrompt] = useState('');
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const generateStory = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/generate', { prompt: prompt, model: 'ollama://llama3.1:latest', });
      setStory(response.data.story);
    } catch (error) {
      console.error('Error generating story:', error);
    }
    setLoading(false);
  };
  return (
    <div className="story-generator">
      <textarea value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Enter your story idea..." />
      <button onClick={generateStory} disabled={loading}>{loading ? 'Generating...' : 'Generate Story'}</button>
      {story && (<div className="story-output">{story}</div>)}
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
    cmd = ['python', 'Write.py', '-Prompt', prompt, '-InitialOutlineModel', model]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return jsonify({'success': True, 'story': result.stdout})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
#### Simple HTML Template (Flask)
...(existing content continues)...

### Minimal React Frontend (Ready-to-Copy)
...(see previous sections)...

---

## 🗄️ Database Integration

StoryForge supports database integration for persistent, professional, and collaborative story management. Integrating a database allows for:
- Saving and retrieving collaborative fiction, story drafts, and chat history.
- Supporting multi-user scenarios with robust access and version control.
- Scaling beyond local sessions for sharing, analytics, and enhancements.

### Recommended Database Technologies
| Database      | Best For                                 | Benefits                                                         |
|---------------|------------------------------------------|------------------------------------------------------------------|
| PostgreSQL    | Production, scaling, data integrity      | ACID transactions, advanced queries, open source, highly scalable |
| MongoDB       | Schema flexibility, rapid iteration      | JSON-like docs, easy to scale horizontally, good for quick changes|
| SQLite        | Local quick prototyping and development  | Zero config, files only, perfect for single-user/testing          |

**Professional Recommendation:** For production and collaborative deployments, PostgreSQL is recommended for its reliability, scalability, active open source community, and broad ecosystem integration. MongoDB is also suitable for teams requiring flexible document structures. SQLite offers a fast local option for prototyping or single-user deployments.

### Integration Overview
1. **Database selection:** Add your chosen backend database engine (install `psycopg2` for PostgreSQL, `pymongo` for MongoDB, or use built-in `sqlite3`).
2. **Environment config:** Store your database URI/credentials in a `.env` file or your hosting provider’s secret manager.
3. **Backend update:**
   - Use SQLAlchemy (recommended for Python) or direct driver for database operations.
   - Add tables/collections for:
     - Users & sessions
     - Stories, chapters, revisions
     - Chat logs/history
   - Example: Automatically store new story generations and chat turns.
4. **Migration:**
   - For PostgreSQL: Run `alembic` migrations or `psql` scripts to create initial schema.
   - For MongoDB: Use `mongo` shell or Mongoose/ODM for schema setup if needed.
   - For SQLite: Python will create the DB file and tables on first run if using SQLAlchemy.
5. **Frontend:**
   - Add features for user login, accessing saved stories, loading project/chat history.

#### Sample Table Structure (PostgreSQL/SQLAlchemy)
```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('User')
```

### Storing Story and Chat History
- **Stories:** Each story, draft, or revision is saved in the database for easy retrieval and collaborative editing.
- **Chat History:** User and AI interactions are logged (with timestamp, author, and content) to track development over time.
- **Collaborators:** Use access control or locking (PostgreSQL-level or simple field flag) for live multi-user coordination.

---

### Integration Notes
- Ensure the backend CLI (`Write.py`) is accessible from your frontend server
- Configure CORS properly if running React and Flask separately
- Consider adding authentication for production deployments
- Implement proper error handling and loading states
- Add file upload support for prompt files
