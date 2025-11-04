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
| Hardware     | Model        | Generation Time | Quality   |
|-------------|-------------|----------------|-----------|
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
(See previous README section for an example React component.)

#### Flask Backend Wrapper
(See previous README section for a Flask backend snippet using Flask and Flask-CORS.)

## 🗄️ Database Integration

StoryForge supports database integration for persistent, professional, and collaborative story management. Integrating a database allows for:

- Saving and retrieving collaborative fiction, story drafts, and chat history.
- Supporting multi-user scenarios with robust access and version control.
- Scaling beyond local sessions for sharing, analytics, and enhancements.

### Recommended Database Technologies
| Database   | Best For    | Benefits                                                          |
|------------|------------|-------------------------------------------------------------------|
| PostgreSQL | Production, scaling, data integrity | ACID transactions, advanced queries, open source, highly scalable |
| MongoDB    | Schema flexibility, rapid iteration | JSON-like docs, easy to scale horizontally, good for quick changes |
| SQLite     | Local quick prototyping and development | Zero config, files only, perfect for single-user/testing          |

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

## 🔐 Authentication & Authorization

StoryForge supports professional authentication integration for both Flask and React platforms, enabling secure and scalable user management. Authentication is essential for production apps to safeguard access to stories, chats, and user-specific features.

### Proven Authentication Strategies
- **Session-Based Authentication:** Recommended for traditional web apps (e.g., Flask backends) using secure server-side session cookies.
- **Token-Based Authentication:** JWT (JSON Web Token)-based authentication for modern APIs and SPA frontends (e.g., React), offering stateless, scalable security.
- **OAuth Integrations:** Enable "sign in with Google" or "sign in with GitHub" for convenient, secure third-party authentication, reducing credential management overhead.

### Recommended Libraries
- **Flask:**
  - [`Flask-Login`](https://flask-login.readthedocs.io/): Session management and user authentication.
  - [`Flask-JWT-Extended`](https://flask-jwt-extended.readthedocs.io/): Token-based user authentication (JWT support).
  - [`Authlib`](https://docs.authlib.org/): Secure OAuth client/provider implementation for Flask (supports Google, GitHub, etc.).
- **React (Node.js/Express backend):**
  - [`Passport.js`](http://www.passportjs.org/): Pluggable authentication for Node.js, supports local (custom), Google, GitHub, JWT, and more.
  - [`jsonwebtoken`](https://github.com/auth0/node-jsonwebtoken): JWT support for signing/verifying tokens.

### Summary of Library Features
| Library             | Features                                                    |
|---------------------|-------------------------------------------------------------|
| Flask-Login         | Session-based auth, login required for routes, user loading |
| Flask-JWT-Extended  | JWT token creation/validation, protected APIs, user claims  |
| Authlib             | OAuth2 and social sign-in flows (Google, GitHub, etc.)      |
| Passport.js         | Unifies local/JWT/OAuth, middleware for Express.js          |
| jsonwebtoken        | Issue and verify JWT tokens for frontend-backend auth       |

### Integration Outline
1. **Backend**
   - Store user credentials and OAuth IDs securely (hashed passwords, no plaintext passwords).
   - Implement user registration (sign up), login, and password reset endpoints.
   - For Flask: Use Flask-Login for session or Flask-JWT-Extended for token auth.
   - For OAuth: Configure Authlib (Flask) or Passport.js (Node) with Google/GitHub client IDs/secrets. Redirect users to authorize, handle callback, store OAuth ID.
   - Issue JWT or set secure session cookie after successful login.
2. **Database**
   - Users table/collection: unique username/email, hashed password/s, OAuth provider IDs.
   - Sessions/JWTs can be optionally stored/tracked for logging/invalidation.
3. **Frontend**
   - Sign up/login React components. Post credentials to backend endpoints.
   - Google/GitHub login: Redirect to OAuth, handle backend response, persist JWT/token in local storage (or use HTTP-only cookie).
   - Protect routes (e.g., Story, Chat) by requiring token/session on the frontend (React routeguards, Flask decorators like `@login_required`).

### Example Protected Route (Flask)
```python
from flask_login import login_required
@app.route('/stories')
@login_required
def user_stories():
    ...
```

### Example JWT Auth Middleware (React/Express)
```js
// Express protected route example
const jwt = require('jsonwebtoken');
function authenticateJWT(req, res, next) {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  if (!token) return res.status(401).json({error: 'No token'});
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({error: 'Invalid token'});
    req.user = user;
    next();
  });
}
app.get('/api/stories', authenticateJWT, (req, res) => {
  // User is authenticated and req.user is set
});
```

---

## Integration Notes
- Ensure the backend CLI (`Write.py`) is accessible from your frontend server
- Configure CORS properly if running React and Flask separately
- Implement authentication and protect all sensitive/story/chat endpoints
- Add frontend loading/error states for authentication
- Add file upload support for prompt files
