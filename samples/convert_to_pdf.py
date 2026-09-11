"""
Convert sample complaint text files to PDF format for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from pathlib import Path
import os

def text_to_pdf(input_file, output_file):
    """Convert a text file to PDF"""
    # Read the text file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        fontName='Courier'
    )
    
    # Split content into paragraphs
    paragraphs = content.split('\n')
    
    for para in paragraphs:
        if para.strip():  # If not empty line
            # Escape special characters for reportlab
            para_text = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            p = Paragraph(para_text, normal_style)
            elements.append(p)
        else:
            elements.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(elements)
    print(f"Created: {output_file}")

def main():
    # Get all .txt files in current directory
    current_dir = Path(__file__).parent
    txt_files = list(current_dir.glob("complaint_*.txt"))
    
    if not txt_files:
        print("No complaint text files found!")
        return
    
    print(f"Found {len(txt_files)} text files to convert...")
    
    for txt_file in txt_files:
        # Create PDF filename
        pdf_file = txt_file.with_suffix('.pdf')
        
        try:
            text_to_pdf(str(txt_file), str(pdf_file))
        except Exception as e:
            print(f"Error converting {txt_file.name}: {e}")
    
    print("\nConversion complete!")
    print(f"PDF files created in: {current_dir}")

if __name__ == "__main__":
    # Check if reportlab is installed
    try:
        import reportlab
        main()
    except ImportError:
        print("reportlab library not found.")
        print("Install it with: pip install reportlab")
        print("\nAlternatively, you can use the text files directly")
        print("or convert them to PDF using any online converter.")
