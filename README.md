# 🔥 StoryForge

[![Hacktoberfest 2025](https://img.shields.io/badge/Hacktoberfest-2025-blueviolet)](https://hacktoberfest.com/)

> **Transform your imagination into epic novels with AI-powered storytelling**

## 🎃 Hacktoberfest 2025 Participant

**This repository is participating in Hacktoberfest 2025!** We welcome quality contributions from developers of all skill levels.

- ✅ All merged PRs will be labeled `hacktoberfest-accepted`
- 🏆 Contributors can claim [Holopin badges](https://holopin.io/) for their contributions
- 📋 Check our [Issues](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) for beginner-friendly tasks

**New to open source?** This is a great place to start! Read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

StoryForge is an advanced AI story generator that creates full-length, coherent novels from simple prompts. Whether you're a writer seeking inspiration, a game master crafting campaigns, or simply someone who loves great stories, StoryForge brings your ideas to life with remarkable depth and creativity.

## ✨ Features

- 📚 **Full-Length Novels** - Generate complete stories with multiple chapters, character arcs, and satisfying conclusions
- 🎭 **Multi-Genre Support** - Fantasy, sci-fi, mystery, romance, adventure, and hybrid genres
- 🏠 **100% Local Processing** - Your stories remain private on your machine
- 📄 **PDF Export** - Professional formatting for easy reading and sharing
- 🌐 **Web Interface** - Clean, intuitive Gradio-based UI accessible via browser
- ⚡ **Smart Generation** - Context-aware storytelling that maintains character consistency
- 🔧 **Highly Customizable** - Extensive configuration options for advanced users

## 🚀 Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Anand0295/-StoryForge.git
cd -StoryForge

# Install Ollama (for local AI models)
curl -fsSL https://ollama.com/install.sh | sh

# Generate your first story
python run_story.py prompts/example_fantasy.txt
```

### Web Interface

Try StoryForge instantly without installation:

**🌐 [Launch StoryForge Web App](https://huggingface.co/spaces/Anand295/StoryForge)**

## 📋 System Requirements

### Minimum Requirements
- **RAM**: 4GB available
- **Storage**: 3GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Model**: `llama3.2:latest` (2GB download)

### Recommended Setup
- **RAM**: 8GB+ available
- **GPU**: NVIDIA RTX series or Apple Silicon
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
  -ChapterWriterModel "ollama://llama3.1:latest" \
  -ExpandOutline

# Quick generation with simple runner
python run_story.py prompts/example_fantasy.txt
```

### Web Interface

1. **Launch the app**: `python app.py` (for local) or visit the [Hugging Face Space](https://huggingface.co/spaces/Anand295/StoryForge)
2. **Enter your prompt**: Describe your story idea in the text box
3. **Generate**: Click the generate button and wait for your novel
4. **Download**: Get your story as a formatted PDF

### Configuration

Customize generation settings in `Writer/Config.py`:

```python
# Model Selection
INITIAL_OUTLINE_WRITER_MODEL = "ollama://llama3.2:latest"
CHAPTER_WRITER_MODEL = "ollama://llama3.2:latest"

# Quality Settings
OUTLINE_MAX_REVISIONS = 3
CHAPTER_MAX_REVISIONS = 2

# Output Options
EXPAND_OUTLINE = True
ENABLE_FINAL_EDIT_PASS = True
```

## 🏗️ Architecture

StoryForge uses a multi-stage generation pipeline for high-quality output:

```mermaid
graph LR
    A[User Prompt] --> B[Context Analysis]
    B --> C[Story Elements]
    C --> D[Outline Generation]
    D --> E[Chapter Writing]
    E --> F[Quality Review]
    F --> G[Final Story]
    G --> H[PDF Export]
```

### Generation Pipeline

1. **Prompt Analysis** - Extract genre, characters, setting, and themes
2. **Story Elements** - Generate character profiles, world-building, and plot structure
3. **Outline Creation** - Develop chapter-by-chapter story progression
4. **Chapter Writing** - Generate detailed narrative content with dialogue and description
5. **Quality Assurance** - Review for consistency, pacing, and coherence
6. **Final Assembly** - Combine chapters into complete novel with formatting

## 🎨 Customization

### Model Configuration
- **Swap Models**: Use different Ollama models for various generation stages
- **Performance Tuning**: Adjust context length, temperature, and other parameters
- **Quality Control**: Configure revision cycles and quality thresholds

### Prompt Engineering
- **Genre Specification**: Include specific genre keywords for better targeting
- **Character Details**: Provide character backgrounds and motivations
- **Setting Description**: Add world-building elements and atmosphere
- **Tone Control**: Specify desired mood, style, and narrative voice

## 📊 Performance

### Generation Quality
- ✅ **Narrative Coherence** - Maintains plot consistency across chapters
- ✅ **Character Development** - Tracks character growth and relationships
- ✅ **Genre Adherence** - Follows genre conventions and tropes appropriately
- ✅ **Pacing Control** - Balances action, dialogue, and description

### Known Limitations
- **Context Memory** - Very long stories may have minor consistency issues
- **Repetition** - Occasional phrase repetition in longer works
- **Complex Plots** - Intricate multi-threaded plots may need manual guidance

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports
- Use the [issue tracker](https://github.com/Anand0295/-StoryForge/issues) to report bugs
- Include system information, error messages, and reproduction steps
- Check existing issues before creating new ones

### 💡 Feature Requests
- Suggest new features or improvements via GitHub issues
- Provide detailed use cases and expected behavior
- Consider contributing code if you have the skills!

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 Documentation
- Improve README, code comments, or user guides
- Add examples and tutorials
- Translate documentation to other languages

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

- ✅ **Use** - Free for personal and commercial use
- ✅ **Modify** - Adapt the code to your needs
- ✅ **Distribute** - Share your modifications
- ⚠️ **Copyleft** - Derivative works must use the same license
- ⚠️ **Network Use** - Server-side usage requires source disclosure

See the [LICENSE](LICENSE) file for full details.

## 🙏 Acknowledgments

- **Ollama Team** - For making local AI accessible
- **Gradio** - For the excellent web interface framework
- **Community Contributors** - For bug reports, features, and feedback

---

<div align="center">

**Happy storytelling! 📚✨**

*Transform your imagination into epic tales with StoryForge*

[🌐 Try Online](https://huggingface.co/spaces/Anand295/StoryForge) • [📖 Documentation](https://github.com/Anand0295/-StoryForge/wiki) • [💬 Discussions](https://github.com/Anand0295/-StoryForge/discussions)

</div>
