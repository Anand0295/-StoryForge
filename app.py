import gradio as gr
import os
import sys
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import subprocess
import time

def generate_story(prompt_text, progress=gr.Progress()):
    """Generate story from user prompt"""
    if not prompt_text.strip():
        return "Please enter a story prompt!", None
    
    progress(0.1, desc="Setting up...")
    
    # Create temp prompt file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(prompt_text)
        prompt_file = f.name
    
    try:
        progress(0.2, desc="Starting story generation...")
        
        # Run story generator
        result = subprocess.run([
            sys.executable, 'Write.py',
            '-Prompt', prompt_file,
            '-NoChapterRevision',
            '-ExpandOutline'
        ], capture_output=True, text=True, timeout=300)
        
        progress(0.8, desc="Finalizing story...")
        
        if result.returncode != 0:
            return f"Error generating story: {result.stderr}", None
        
        # Find generated story file
        output_dir = "Output"
        if os.path.exists(output_dir):
            story_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            if story_files:
                latest_file = max([os.path.join(output_dir, f) for f in story_files], 
                                key=os.path.getctime)
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    story_content = f.read()
                
                progress(0.9, desc="Creating PDF...")
                pdf_path = create_pdf(story_content, prompt_text[:50])
                
                progress(1.0, desc="Complete!")
                return story_content, pdf_path
        
        return "Story generated but output file not found.", None
        
    except subprocess.TimeoutExpired:
        return "Story generation timed out. Try a shorter prompt.", None
    except Exception as e:
        return f"Error: {str(e)}", None
    finally:
        # Clean up temp file
        if os.path.exists(prompt_file):
            os.unlink(prompt_file)

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
        alignment=1  # Center
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
    "Write a fantasy adventure about a young mage discovering an ancient prophecy that threatens to destroy their kingdom.",
    "Create a sci-fi thriller about a space colony that loses contact with Earth and discovers they're not alone.",
    "Tell a mystery story about a detective investigating strange disappearances in a small coastal town.",
    "Write a romance novel about two rival chefs competing in a cooking competition.",
    "Create an adventure story about explorers finding a lost civilization in the Amazon rainforest."
]

# Create Gradio interface
with gr.Blocks(title="🔥 StoryForge - AI Novel Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔥 StoryForge
    *Generate full-length novels with AI - locally powered, globally accessible*
    
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
        fn=generate_story,
        inputs=[prompt_input],
        outputs=[story_output, pdf_output],
        show_progress=True
    )
    
    gr.Markdown("""
    ---
    ### 🎯 How it works:
    1. **Enter your prompt** - Describe the story you want
    2. **Click Generate** - AI creates a full novel (this may take a few minutes)
    3. **Read & Download** - View your story and download as PDF
    
    ### ⚡ Tips for better stories:
    - Be specific about genre, characters, and setting
    - Include conflict or challenges for characters to overcome  
    - Mention the tone you want (dark, humorous, romantic, etc.)
    
    *Powered by local AI models - your stories stay private!*
    """)

if __name__ == "__main__":
    demo.launch()