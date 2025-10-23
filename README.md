# 🔥 StoryForge

*Because your imagination deserves better than writer's block* ✍️

Turn a simple prompt into a full-blown novel using the power of local AI. No cloud dependencies, no API keys, no drama - just pure storytelling magic running on your machine.

## ✨ What Makes This Special?

🏠 **100% Local** - Your stories stay on your computer (where they belong)  
🚀 **Zero Setup Hassle** - Install Ollama, run script, get novel  
🎭 **Actually Coherent** - Characters remember their own names (revolutionary!)  
📖 **Novel-Length Output** - Not just "once upon a time, the end"  
🔧 **Stupidly Customizable** - Tweak everything or change nothing  
🌍 **Cross-Platform** - Works on whatever OS you're stuck with  

## 🎯 Quick Start (Seriously, It's Easy)

```bash
# 1. Get Ollama (if you haven't already)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Clone this bad boy
git clone https://github.com/Anand0295/-StoryForge.git
cd -StoryForge

# 3. Generate your masterpiece
./run_story.py
```

*That's it. No, really. The AI will handle the rest.*

## 💻 Will This Melt My Computer?

**TL;DR:** Probably not, but here's what you need:

- **Potato PC**: Use `llama3.2:latest` (2GB) - it's surprisingly decent
- **Gaming Rig**: Go wild with `llama3.1:latest` (5GB) for better quality  
- **NASA Supercomputer**: You're probably overqualified for this

*Check [Model Recommendations](Docs/Models.md) if you want the nerdy details.*

## 🎮 Usage (Choose Your Adventure)

### The "I Just Want Stories" Method
```bash
./run_story.py  # Uses sensible defaults
```

### The "I Know What I'm Doing" Method
```bash
./Write.py -Prompt prompts/your_prompt.txt -InitialOutlineModel "ollama://llama3.2:latest"
```

### The "I Live Dangerously" Method
Edit `Writer/Config.py` and change whatever you want:
```python
INITIAL_OUTLINE_WRITER_MODEL = "ollama://llama3.2:latest"
CHAPTER_WRITER_MODEL = "ollama://llama3.2:latest"
# Go nuts
```

## 🎨 How It Works (The Magic Explained)

```
Your Prompt → AI Brainstorms → Creates Outline → Writes Chapters → Novel!
```

*It's like having a writing buddy who never gets tired, never judges your weird ideas, and works for free.*

## 🔧 Customization (For the Tinkerers)

- **Model Swapping**: Try different Ollama models - some are fast, some are smart, some are both
- **Prompt Engineering**: Write better prompts, get better stories (shocking, I know)
- **Config Tweaking**: Dive into `Writer/Config.py` and break things responsibly

## ✅ What Actually Works

- **Length**: Generates proper novels, not Twitter threads
- **Consistency**: Characters don't randomly change names halfway through  
- **Coherence**: Plot actually makes sense (most of the time)
- **Speed**: Fast enough that you won't die of old age waiting

## 🚧 Known "Features"

- Sometimes gets a bit repetitive (working on it)
- Occasionally forgets what happened 3 chapters ago (also working on it)
- May generate stories better than your last attempt (not working on fixing this)

## 🤝 Want to Help?

**Found a bug?** Open an issue (please include what you broke and how)  
**Have ideas?** Share them! Weird ideas are the best ideas  
**Code improvements?** Pull requests welcome (just don't break everything)  
**Success stories?** Tell us about the novel you generated that's better than Twilight  

*Seriously though, feedback is gold. Even if it's just "this is cool" or "this is terrible."*

## 📄 Legal Stuff

AGPL-3.0 License - Use it, modify it, share it. Just don't be evil.

---

**Happy writing! May your plots be thick and your characters thicker.** 📚✨

*P.S. - If this generates the next bestseller, a coffee would be nice ☕*
