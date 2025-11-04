import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/generate', {
        prompt: inputValue,
        model: 'ollama://llama3.1:latest'
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.story || response.data.error || 'No response received',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Add to conversation history
      if (conversations.length === 0 || messages.length === 0) {
        setConversations(prev => [...prev, {
          id: Date.now(),
          title: inputValue.substring(0, 30) + '...',
          timestamp: new Date().toISOString()
        }]);
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Error: Could not generate story. Make sure the Flask backend is running on http://localhost:5000',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  const startNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <button className="new-chat-btn" onClick={startNewChat}>
          <span className="plus-icon">+</span>
          New Story
        </button>
        
        <div className="conversation-list">
          {conversations.map(conv => (
            <div key={conv.id} className="conversation-item">
              <div className="conversation-icon">💬</div>
              <span className="conversation-title">{conv.title}</span>
            </div>
          ))}
        </div>
        
        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">👤</div>
            <span className="user-name">StoryForge User</span>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-content">
        <div className="chat-header">
          <h1>StoryForge AI</h1>
          <p className="subtitle">Generate amazing stories with AI</p>
        </div>

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-screen">
              <h2>🔥 Welcome to StoryForge</h2>
              <p>Start generating your stories by entering a prompt below</p>
              <div className="example-prompts">
                <div className="example-prompt">"Write a sci-fi story about time travel"</div>
                <div className="example-prompt">"Create a fantasy adventure with dragons"</div>
                <div className="example-prompt">"Tell a mystery story set in Victorian London"</div>
              </div>
            </div>
          ) : (
            messages.map((message, index) => (
              <div key={index} className={`message ${message.role} ${message.isError ? 'error' : ''}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="message assistant">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="loading-indicator">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-container">
          <form onSubmit={handleSubmit} className="input-form">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter your story prompt..."
              className="input-textarea"
              rows="1"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={loading || !inputValue.trim()}
            >
              {loading ? '⏳' : '➤'}
            </button>
          </form>
          <p className="input-footer">StoryForge can make mistakes. Consider checking important information.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
