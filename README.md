#
 🔥 StoryForge
>
 
**
Transform your imagination into epic novels with AI-powered storytelling
**
StoryForge is an advanced AI story generator that creates full-length, coherent novels from simple prompts. Whether you're a writer seeking inspiration, a game master crafting campaigns, or simply someone who loves great stories, StoryForge brings your ideas to life with remarkable depth and creativity.
##
 ✨ Features
-
 📚 
**
Full-Length Novels
**
 - Generate complete stories with multiple chapters, character arcs, and satisfying conclusions
-
 🎭 
**
Multi-Genre Support
**
 - Fantasy, sci-fi, mystery, romance, adventure, and hybrid genres
-
 🏠 
**
100% Local Processing
**
 - Your stories remain private on your machine
-
 📄 
**
PDF Export
**
 - Professional formatting for easy reading and sharing
-
 🌐 
**
Web Interface
**
 - Clean, intuitive Gradio-based UI accessible via browser
-
 ⚡ 
**
Smart Generation
**
 - Context-aware storytelling that maintains character consistency
-
 🔧 
**
Highly Customizable
**
 - Extensive configuration options for advanced users
##
 🚀 Quick Start
###
 Local Installation
```
bash
# Clone the repository
git clone https://github.com/Anand0295/-StoryForge.git
cd -StoryForge
# Install Ollama (for local AI models)
curl -fsSL https://ollama.com/install.sh | sh
# Generate your first story
python run_story.py prompts/example_fantasy.txt
```
###
 Web Interface
Try StoryForge instantly without installation:
**
🌐 
[
Launch StoryForge Web App
]
(
https://huggingface.co/spaces/Anand295/StoryForge
)
**
##
 📋 System Requirements
###
 Minimum Requirements
-
 
**
RAM
**
: 4GB available
-
 
**
Storage
**
: 3GB free space
-
 
**
OS
**
: Windows 10+, macOS 10.14+, or Linux
-
 
**
Model
**
: 
`
llama3.2:latest
`
 (2GB download)
###
 Recommended Setup
-
 
**
RAM
**
: 8GB+ available
-
 
**
GPU
**
: NVIDIA RTX series or Apple Silicon
-
 
**
Model
**
: 
`
llama3.1:latest
`
 (5GB download)
-
 
**
Storage
**
: 10GB+ for multiple models
###
 Performance Guide
|
 Hardware 
|
 Model 
|
 Generation Time 
|
 Quality 
|
|----------|-------|-----------------|----------|
|
 CPU Only 
|
 llama3.2 
|
 5-10 min 
|
 Good 
|
|
 RTX 3060+ 
|
 llama3.1 
|
 2-5 min 
|
 Excellent 
|
|
 Apple M1+ 
|
 llama3.1 
|
 3-7 min 
|
 Excellent 
|
##
 🎯 Usage
###
 Command Line Interface
```
bash
# Basic usage with default settings
python Write.py -Prompt "Your story idea here"
# Advanced usage with custom models
python Write.py -Prompt prompts/fantasy.txt \
  -InitialOutlineModel "ollama://llama3.1:latest" \
