# 🔥 StoryForge

> **Transform your imagination into epic novels with AI-powered storytelling**

StoryForge is an advanced AI story generator that creates full-length, coherent novels from simple prompts. Whether you're a writer seeking inspiration, a game master crafting campaigns, or simply someone who loves great stories, StoryForge brings your ideas to life with remarkable depth and creativity.

## ✨ Features

- 📚 **Full-Length Novels** - Generate complete stories with multiple chapters, character arcs, and satisfying conclusions
- 🎭 **Multi-Genre Support** - Fantasy, sci-fi, mystery, romance, adventure, and hybrid genres
- 🏠 **100% Local Processing** - Your stories remain private on your machine
- 📄 **PDF Export** - Professional formatting for easy reading and sharing
- 🌐 **Web Interface** - Clean, intuitive UI accessible via browser
- ⚡ **Smart Generation** - Context-aware storytelling that maintains character consistency
- 🔧 **Highly Customizable** - Extensive configuration options for advanced users
- 🚀 **Lightweight & Fast** - Optimized for local execution with minimal dependencies

## ⚡ Quick Start (Solo Dev/Local)

```bash
# Clone and setup
git clone https://github.com/Anand0295/-StoryForge.git
cd -StoryForge
pip install -r requirements.txt

# Run directly (CPU mode)
python Write.py -Prompt "Your story idea"

# Or with GPU acceleration (NVIDIA CUDA or Apple M1+)
CUDA_VISIBLE_DEVICES=0 python Write.py -Prompt "Your story idea"
```

## 📦 Installation

### Prerequisites

- **Python**: 3.8+
- **RAM**: 8GB minimum, 16GB recommended
- **GPU** (Optional but recommended): NVIDIA RTX series or Apple Silicon
- **Model**: `llama3.2:latest` or lightweight alternative (2-5GB)
- **Storage**: 5GB+ for base model

### Performance Guide

| Hardware | Model | Generation Time | Quality |
|----------|-------|-----------------|----------|
| CPU Only | llama3.2 | 5-10 min | Good |
| RTX 3060+ | llama3.2 | 1-3 min | Excellent |
| Apple M1+ | llama3.2 | 2-4 min | Excellent |

### Hardware Acceleration Setup

#### NVIDIA GPU (CUDA)

```bash
# Verify CUDA availability
nvcc --version

# Enable GPU in your script
CUDA_VISIBLE_DEVICES=0 python Write.py -Prompt "story"
```

#### Apple Silicon (Metal)

```bash
# Metal acceleration enabled by default on M1/M2/M3+
python Write.py -Prompt "story"
```

## 🎯 Usage

### Command Line Interface

```bash
# Basic usage with default settings
python Write.py -Prompt "Your story idea here"

# Advanced usage with custom models
python Write.py -Prompt prompts/fantasy.txt \
  -InitialOutlineModel "ollama://llama3.2:latest" \
  -ChapterModel "ollama://llama3.2:latest"

# For production deployment with gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

## 🖥️ Backend Optimization

### Lightweight Dependencies

StoryForge uses a minimal dependency footprint:
- **Flask** (or FastAPI) - Web framework
- **Ollama SDK** - Local LLM integration
- **ReportLab** - PDF generation
- No heavy ML frameworks required for inference

### Production Server Setup

#### Option 1: Gunicorn (Flask)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 300 app:app
```

#### Option 2: Uvicorn (FastAPI/Async)

```bash
pip install uvicorn
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 4
```

### AI Model Selection

For local execution, use lightweight models:
- **llama3.2** - 3.2B params, excellent balance
- **mistral:7b** - 7B params, high quality
- **neural-chat** - 7B params, fast response

Avoid heavy models (13B+) for single-machine deployment.

### Async/Threaded Server

```python
# Use async for non-blocking I/O
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/generate")
async def generate_story(prompt: str):
    # Non-blocking generation
    return StreamingResponse(generate_chunks(prompt))
```

## 🌐 Frontend Creation

### Recommended Stack

#### React + Vite (Recommended)

- **Framework**: React.js with Vite (sub-second HMR)
- **UI Library**: Tailwind CSS (tree-shaking for minimal bundle)
- **State Management**: React Context (no Redux bloat)
- **API Communication**: Fetch API or Axios
- **Build Output**: ~50KB gzipped (vs 200KB with CRA)

### Frontend Optimization

#### Vite Build Setup

```bash
npm create vite@latest storyforge-frontend -- --template react
cd storyforge-frontend
npm install
```

#### Vite Configuration (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom']
        }
      }
    },
    chunkSizeWarningLimit: 500
  }
})
```

#### Lazy Loading Components

```javascript
import { lazy, Suspense } from 'react';

const StoryEditor = lazy(() => import('./pages/StoryEditor'));
const ChatHistory = lazy(() => import('./pages/ChatHistory'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <StoryEditor />
      <ChatHistory />
    </Suspense>
  );
}
```

#### Asset Compression

```bash
# Install compression tools
npm install --save-dev vite-plugin-compression

# Images: Use modern formats
# Convert PNG/JPG to WebP
# cwebp image.png -o image.webp
```

#### Performance Targets

- **Bundle Size**: < 150KB gzipped
- **First Contentful Paint**: < 2s
- **Lazy-loaded chunks**: < 50KB each

### Flask Minimal Interface (Optional)

```bash
pip install flask flask-cors
mkdir storyforge_web && cd storyforge_web
touch app.py
mkdir templates static
```

## 🗄️ Database Integration

StoryForge supports flexible database options for persistent story management.

### Default: SQLite (Local Dev)

**Recommended for solo dev and prototyping:**

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = sqlite3.connect('storyforge.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Tables created automatically on first run
def init_db():
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')
        conn.commit()
```

### Scaling to PostgreSQL

**When ready for production/multi-user:**

```bash
# Install PostgreSQL driver
pip install psycopg2-binary sqlalchemy
```

```python
from sqlalchemy import create_engine

# Development (SQLite)
engine = create_engine('sqlite:///storyforge.db')

# Production (PostgreSQL)
engine = create_engine(
    'postgresql://user:password@localhost:5432/storyforge',
    pool_size=20,
    max_overflow=40
)
```

### Recommended Databases

| Database | Use Case | Benefits |
|----------|----------|----------|
| SQLite | Local dev, solo use | Zero config, file-based, fast for <1GB data |
| PostgreSQL | Production, multi-user | ACID, advanced queries, horizontal scaling |
| MongoDB | Rapid iteration, flexible schema | JSON docs, horizontal scaling |

### Sample Table Structure (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    stories = relationship('Story', back_populates='user')

class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('User', back_populates='stories')
```

## 📦 Deployment

### Single-Binary Packaging

#### PyInstaller Build

```bash
pip install pyinstaller
pyinstaller --onefile --collect-all ollama Write.py

# Output: dist/Write (Linux/Mac) or dist/Write.exe (Windows)
```

#### Distribution

```bash
# Create portable package
zip -r storyforge-bundle.zip dist/Write models/ templates/
# Users extract and run: ./Write or ./Write.exe
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔐 Authentication & Authorization

For multi-user deployments, integrate secure authentication:

### Session-Based (Flask)

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/stories')
@login_required
def user_stories():
    return jsonify(current_user.stories)
```

### Token-Based (JWT)

```python
from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
```

## 📝 Integration Notes

- Backend CLI (`Write.py`) runs independently or via Flask/FastAPI wrapper
- Configure CORS if running separate frontend/backend
- Implement authentication for multi-user scenarios
- Use SQLite for local dev, PostgreSQL for production
- Enable hardware acceleration (CUDA/Metal) for 3-5x speedup
- Lazy-load frontend components for sub-2s initial load
- Deploy with gunicorn/uvicorn, not Flask development server

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests.

---

**Optimized for lightweight, fast native execution - Perfect for solo developers and local deployments.**
