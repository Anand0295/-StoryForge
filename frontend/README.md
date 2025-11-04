# StoryForge Frontend

A professional ChatGPT-style frontend for the StoryForge AI story generator, built with React and Vite.

## Features

- 🎨 **ChatGPT-Inspired UI**: Clean, modern interface with dark theme
- 📱 **Responsive Design**: Sidebar navigation with conversation history
- 💬 **Chat Interface**: Conversational UI for story generation
- ⚡ **Real-time Updates**: Loading indicators and error handling
- 🔄 **Backend Integration**: Connects to Flask backend API

## Tech Stack

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls
- **CSS3**: Custom styling inspired by ChatGPT

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main application component
│   ├── App.css          # Application styles
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
└── .gitignore          # Git ignore rules
```

## Installation

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## Backend Setup

Make sure the Flask backend is running before using the frontend:

1. Navigate to the project root
2. Install Flask dependencies:
   ```bash
   pip install flask flask-cors
   ```

3. Start the Flask backend:
   ```bash
   python app.py
   ```

   The backend should run on `http://localhost:5000`

## Usage

1. Start both the frontend (port 3000) and backend (port 5000)
2. Open your browser to `http://localhost:3000`
3. Enter a story prompt in the input field
4. Click send or press Enter to generate a story
5. View your generated stories in the chat interface

## Features in Detail

### Sidebar
- **New Story**: Start a fresh conversation
- **Conversation History**: View past story prompts
- **User Profile**: Display user information

### Chat Area
- **Welcome Screen**: Shows example prompts when no messages
- **Message Display**: User prompts and AI responses in chat bubbles
- **Loading Indicator**: Animated dots while generating
- **Error Handling**: Clear error messages if backend is unavailable

### Input Area
- **Multi-line Input**: Textarea for longer prompts
- **Send Button**: Submit prompts (disabled while loading)
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line

## API Integration

The frontend connects to the Flask backend's `/generate` endpoint:

```javascript
POST http://localhost:5000/generate
Body: {
  prompt: string,
  model: string
}
```

## Building for Production

To create a production build:

```bash
npm run build
```

The optimized files will be in the `dist/` directory.

## Customization

### Styling
- Edit `src/App.css` for component-specific styles
- Edit `src/index.css` for global styles
- Colors and spacing follow ChatGPT's design patterns

### Backend URL
To change the backend URL, update the axios call in `src/App.jsx`:

```javascript
const response = await axios.post('YOUR_BACKEND_URL/generate', {
  prompt: inputValue,
  model: 'ollama://llama3.1:latest'
});
```

## Troubleshooting

**Frontend won't start**:
- Make sure Node.js is installed: `node --version`
- Try removing `node_modules` and reinstalling: `npm install`

**Can't connect to backend**:
- Verify Flask is running on port 5000
- Check CORS is enabled in Flask backend
- Verify the backend URL in `App.jsx`

**Build errors**:
- Clear cache: `rm -rf node_modules dist`
- Reinstall dependencies: `npm install`

## Contributing

Contributions are welcome! Please follow the project's coding standards and submit pull requests for any enhancements.

## License

AGPL-3.0 - See the main project LICENSE file for details.
