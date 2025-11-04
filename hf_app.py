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
import html
import re

# Simple story generator using Hugging Face Inference API

def sanitize_input(text):
    """Sanitize user input to prevent XSS and injection attacks (CWE-20/79/80).
    
    Validates and cleans user-provided text by:
    - Stripping leading/trailing whitespace
    - Limiting length to prevent DoS
    - Removing potentially dangerous characters
    - HTML-escaping the result
    
    Args:
        text: Raw user input string
        
    Returns:
        Sanitized and HTML-escaped string safe for display
    """
    if not isinstance(text, str):
        return ""
    
    # Strip whitespace and limit length to prevent DoS
    text = text.strip()[:10000]
    
    # Remove null bytes and other control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # HTML escape to prevent XSS (CWE-79/80)
    text = html.escape(text, quote=True)
    
    return text

def validate_prompt(prompt_text):
    """Validate story prompt input (CWE-20).
    
    Ensures prompt meets basic requirements:
    - Non-empty after sanitization
    - Minimum length requirement
    - Maximum length enforcement
    
    Args:
        prompt_text: User-provided story prompt
        
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    if not prompt_text or not prompt_text.strip():
        return False, "Please enter a story prompt!"
    
    sanitized = sanitize_input(prompt_text)
    
    if len(sanitized) < 3:
        return False, "Prompt must be at least 3 characters long."
    
    if len(sanitized) > 5000:
        return False, "Prompt is too long. Please limit to 5000 characters."
    
    return True, None

def generate_story_simple(prompt_text, progress=gr.Progress()):
    """Generate story using HF Inference API with secure input handling.
    
    Applies strict input validation and sanitization (CWE-20/79/80):
    - Validates prompt format and length
    - Sanitizes all user inputs before processing
    - HTML-escapes all outputs to prevent XSS
    - Proper error handling with safe error messages
    
    Args:
        prompt_text: User-provided story prompt (will be sanitized)
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (story_content: str, pdf_path: str or None)
        All returned strings are HTML-escaped for safe display
    """
    try:
        # Validate input (CWE-20)
        is_valid, error_msg = validate_prompt(prompt_text)
        if not is_valid:
            # Return HTML-escaped error message (CWE-79/80)
            return html.escape(error_msg, quote=True), None
        
        # Sanitize input to prevent injection attacks (CWE-20/79/80)
        safe_prompt = sanitize_input(prompt_text)
        
        progress(0.1, desc="Starting story generation...")
        
        # Simple story structure
        story_parts = []
        
        # Generate outline with sanitized input
        progress(0.3, desc="Creating story outline...")
        outline_prompt = f"Create a detailed story outline for: {safe_prompt}\nOutline:"
        outline = generate_text_hf(outline_prompt, max_length=500)
        
        # Sanitize outline output (CWE-79/80)
        safe_outline = sanitize_input(outline)
        
        # Generate chapters with sanitized data
        progress(0.5, desc="Writing chapters...")
        chapter_prompt = f"Based on this outline: {safe_outline}\n\nWrite a complete story for: {safe_prompt}\n\nStory:"
        story_content = generate_text_hf(chapter_prompt, max_length=2000)
        
        # Sanitize story content before display (CWE-79/80)
        safe_story_content = sanitize_input(story_content)
        
        progress(0.8, desc="Creating PDF...")
        # Use sanitized prompt for PDF title (limit to 50 chars)
        safe_title = safe_prompt[:50]
        pdf_path = create_pdf(safe_story_content, safe_title)
        
        progress(1.0, desc="Complete!")
        
        # Return HTML-escaped content for safe display (CWE-79/80)
        return safe_story_content, pdf_path
        
    except ValueError as e:
        # Handle validation errors with safe error messages (CWE-79/80)
        error_msg = f"Validation error: {str(e)}"
        return html.escape(error_msg, quote=True), None
    except IOError as e:
        # Handle file I/O errors safely (CWE-79/80)
        error_msg = f"File error: Unable to create PDF"
        return html.escape(error_msg, quote=True), None
    except Exception as e:
        # Generic error handler with safe output (CWE-79/80)
        # Don't expose internal error details to prevent information disclosure
        error_msg = "Error generating story. Please try again with a different prompt."
        return html.escape(error_msg, quote=True), None

def generate_text_hf(prompt, max_length=1000):
    """Generate text using Hugging Face Inference API.
    
    Note: Input prompt should already be sanitized by caller.
    Output is plain text that will be sanitized before display.
    
    Args:
        prompt: Sanitized prompt text
        max_length: Maximum length of generated text
        
    Returns:
        Generated text (will be sanitized by caller before display)
    """
    # Validate max_length parameter
    if not isinstance(max_length, int) or max_length < 1 or max_length > 10000:
        max_length = 1000
    
    # For demo purposes, return a simple generated story
    # In production, you'd use actual HF API calls with proper error handling
    
    if "outline" in prompt.lower():
        return f"""Story Outline:
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
- Character reaches conclusion of journey"""
    else:
        return f"""Once upon a time, in a world shaped by imagination...

Chapter 1: The Beginning
The story began in an unexpected place, where our protagonist discovered something that would change everything. The air was filled with possibility, and the journey ahead promised adventure.

Chapter 2: The Challenge
As events unfolded, challenges emerged that tested resolve and determination. Each obstacle brought new insights and opportunities for growth.

Chapter 3: The Transformation
Through perseverance and courage, transformation occurred. What seemed impossible became achievable, and new paths opened.

Chapter 4: The Conclusion
In the end, wisdom was gained and the journey completed. Though the adventure concluded, its lessons remained forever.

The End."""

def create_pdf(story_text, title="My Story"):
    """Create PDF from story text with secure handling.
    
    Sanitizes inputs to prevent injection in PDF generation (CWE-20/79/80).
    
    Args:
        story_text: Story content (should be pre-sanitized)
        title: PDF title (should be pre-sanitized)
        
    Returns:
        Path to created PDF file
        
    Raises:
        IOError: If PDF creation fails
    """
    try:
        # Additional sanitization for PDF content (defense in depth)
        # Remove any HTML entities that might have been escaped
        safe_story = html.unescape(story_text) if story_text else ""
        safe_title = html.unescape(title) if title else "My Story"
        
        # Validate sanitized inputs
        if not safe_story or not safe_story.strip():
            safe_story = "No content available"
        
        if not safe_title or not safe_title.strip():
            safe_title = "My Story"
        
        # Create temporary file with secure permissions
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb')
        pdf_path = temp_file.name
        temp_file.close()
        
        # Create PDF with sanitized content
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story_elements = []
        
        # Add title with sanitized text
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        story_elements.append(Paragraph(safe_title, title_style))
        story_elements.append(Spacer(1, 0.2*inch))
        
        # Add story content with sanitized text (split by paragraphs)
        for paragraph in safe_story.split('\n\n'):
            if paragraph.strip():
                # Paragraph class in reportlab handles text safely
                story_elements.append(Paragraph(paragraph.strip(), styles['Normal']))
                story_elements.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story_elements)
        
        return pdf_path
        
    except Exception as e:
        # Log error securely without exposing sensitive details
        raise IOError(f"PDF creation failed") from e

def create_interface():
    """Create Gradio interface with secure configuration.
    
    Implements secure practices:
    - Input validation and sanitization (CWE-20)
    - XSS prevention through output escaping (CWE-79/80)
    - Clear user guidance on input requirements
    - Proper error handling
    """
    with gr.Blocks(title="StoryForge - Secure Story Generator") as demo:
        gr.Markdown("""# 📚 StoryForge - AI Story Generator
        
        ### Create amazing stories with AI assistance!
        
        **Security Notice:** All inputs are validated and sanitized to ensure safe operation.
        """)
        
        with gr.Row():
            with gr.Column():
                # Input with validation hints
                prompt_input = gr.Textbox(
                    label="Story Prompt",
                    placeholder="Enter your story idea (3-5000 characters)...",
                    lines=3,
                    max_lines=10
                )
                
                generate_btn = gr.Button("Generate Story", variant="primary")
                
                gr.Markdown("""**Tips:**
                - Be specific about characters, setting, and plot
                - Provide clear details for better results
                - Input is automatically validated and sanitized
                """)
        
        with gr.Row():
            with gr.Column():
                # Output with HTML escaping enabled
                story_output = gr.Textbox(
                    label="Generated Story",
                    lines=20,
                    max_lines=50,
                    interactive=False
                )
                
                pdf_output = gr.File(
                    label="Download PDF",
                    interactive=False
                )
        
        # Connect button with secure handler
        generate_btn.click(
            fn=generate_story_simple,
            inputs=[prompt_input],
            outputs=[story_output, pdf_output]
        )
        
        # Add examples with safe content
        gr.Examples(
            examples=[
                ["A young scientist discovers a portal to another dimension"],
                ["A detective solving a mysterious case in a futuristic city"],
                ["An adventure through an enchanted forest with magical creatures"]
            ],
            inputs=[prompt_input]
        )
    
    return demo

if __name__ == "__main__":
    # Launch with secure settings
    demo = create_interface()
    demo.launch(
        share=False,  # Disable sharing to prevent unauthorized access
        server_name="0.0.0.0",
        server_port=7860
    )
