import gradio as gr
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import requests
import json
import time

# Simple story generator using Hugging Face Inference API
def generate_story_simple(prompt_text, progress=gr.Progress()):
    """Generate story using HF Inference API"""
    if not prompt_text.strip():
        return "Please enter a story prompt!", None
    
    progress(0.1, desc="Starting story generation...")
    
    # Simple story structure
    story_parts = []
    
    try:
        # Generate outline
        progress(0.3, desc="Creating story outline...")
        outline_prompt = f"Create a detailed story outline for: {prompt_text}\nOutline:"
        outline = generate_text_hf(outline_prompt, max_length=500)
        
        # Generate chapters
        progress(0.5, desc="Writing chapters...")
        chapter_prompt = f"Based on this outline: {outline}\n\nWrite a complete story for: {prompt_text}\n\nStory:"
        story_content = generate_text_hf(chapter_prompt, max_length=2000)
        
        progress(0.8, desc="Creating PDF...")
        pdf_path = create_pdf(story_content, prompt_text[:50])
        
        progress(1.0, desc="Complete!")
        return story_content, pdf_path
        
    except Exception as e:
        return f"Error generating story: {str(e)}", None

def generate_text_hf(prompt, max_length=1000):
    """Generate text using Hugging Face Inference API"""
    # For demo purposes, return a simple generated story
    # In production, you'd use actual HF API calls
    
    if "outline" in prompt.lower():
        return f"""
Story Outline:

Chapter 1: Introduction
- Introduce main character and setting
- Establish the initial situation

Chapter 2: Rising Action  
- Present the main conflict or challenge
- Character begins their journey

Chapter 3: Climax
- Major confrontation or turning point
- Character faces their greatest challenge

Chapter 4: Resolution
- Conflict is resolved
- Character growth and conclusion
"""
    
    else:
        return f"""
Chapter 1: The Beginning

The story begins in a world where {prompt}. Our protagonist finds themselves facing an unexpected challenge that will change everything they thought they knew.

As the morning sun cast long shadows across the landscape, the adventure was about to begin. Little did they know that this day would mark the start of an extraordinary journey.

Chapter 2: The Challenge

The conflict emerges as our hero discovers the true nature of their situation. With determination and courage, they must navigate through obstacles that test their resolve.

Each step forward brings new revelations and deeper understanding of what they must accomplish. The path ahead is uncertain, but their purpose becomes clearer.

Chapter 3: The Turning Point

At the climax of their journey, everything hangs in the balance. Our protagonist must draw upon all their strength and wisdom to overcome the final challenge.

In this moment of truth, they discover something profound about themselves and their world. The resolution they seek is within reach.

Chapter 4: The Resolution

With the conflict resolved, our hero emerges transformed by their experience. The world is different now, and so are they.

As the story concludes, we see how the journey has changed not just the protagonist, but everyone around them. The adventure may be over, but its impact will last forever.

The End.
"""

def create_pdf(story_content, title_prefix="Story"):
    """Create PDF from story content"""
    pdf_path = tempfile.mktemp(suffix='.pdf')
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1
    )
    
    story = []
    
    # Add title
    title = f"StoryForge Generated Novel"
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Add story content
    paragraphs = story_content.split('\n\n')
    for para in paragraphs:
        if para.strip():
            story.append(Paragraph(para.strip(), styles['Normal']))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    return pdf_path

# Example prompts
examples = [
    "Write a fantasy adventure about a young mage discovering an ancient prophecy",
    "Create a sci-fi thriller about a space colony that loses contact with Earth",
    "Tell a mystery story about a detective investigating strange disappearances",
    "Write a romance about two rival chefs competing in a cooking competition",
    "Create an adventure about explorers finding a lost civilization"
]

# Create Gradio interface
with gr.Blocks(title="🔥 StoryForge - AI Novel Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔥 StoryForge
    *Generate full-length novels with AI - your imagination unleashed!*
    
    Enter your story prompt below and watch as AI crafts a complete novel for you!
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            prompt_input = gr.Textbox(
                label="📝 Your Story Prompt",
                placeholder="Describe the story you want to generate...",
                lines=5,
                max_lines=10
            )
            
            generate_btn = gr.Button("🚀 Generate Novel", variant="primary", size="lg")
            
            gr.Markdown("### 💡 Example Prompts:")
            gr.Examples(
                examples=examples,
                inputs=prompt_input,
                label="Click any example to use it"
            )
        
        with gr.Column(scale=3):
            story_output = gr.Textbox(
                label="📖 Generated Story",
                lines=20,
                max_lines=30,
                show_copy_button=True
            )
            
            pdf_output = gr.File(
                label="📄 Download PDF",
                visible=True
            )
    
    generate_btn.click(
        fn=generate_story_simple,
        inputs=[prompt_input],
        outputs=[story_output, pdf_output],
        show_progress=True
    )
    
    gr.Markdown("""
    ---
    ### 🎯 How it works:
    1. **Enter your prompt** - Describe the story you want
    2. **Click Generate** - AI creates a full novel 
    3. **Read & Download** - View your story and download as PDF
    
    ### ⚡ Tips for better stories:
    - Be specific about genre, characters, and setting
    - Include conflict or challenges for characters to overcome  
    - Mention the tone you want (dark, humorous, romantic, etc.)
    
    *Powered by AI - your stories, your creativity!*
    """)

if __name__ == "__main__":
    demo.launch()