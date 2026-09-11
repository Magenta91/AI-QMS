"""
Simple script to create sample PDF files from text files
Uses fpdf2 which is simpler than reportlab
"""
from pathlib import Path

def create_pdfs_simple():
    """Create PDFs using fpdf2"""
    try:
        from fpdf import FPDF
        
        current_dir = Path(__file__).parent
        txt_files = list(current_dir.glob("complaint_*.txt"))
        
        if not txt_files:
            print("No complaint text files found!")
            return
        
        print(f"Found {len(txt_files)} text files to convert...")
        
        for txt_file in txt_files:
            # Read text content
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Courier", size=9)
            
            # Add content
            for line in content.split('\n'):
                # Handle special characters
                try:
                    pdf.cell(0, 4, txt=line, ln=True)
                except:
                    # Skip lines with encoding issues
                    pdf.cell(0, 4, txt=line.encode('latin-1', 'ignore').decode('latin-1'), ln=True)
            
            # Save PDF
            pdf_file = txt_file.with_suffix('.pdf')
            pdf.output(str(pdf_file))
            print(f"Created: {pdf_file.name}")
        
        print("\nConversion complete!")
        print(f"PDF files created in: {current_dir}")
        
    except ImportError:
        print("fpdf2 library not found.")
        print("Install it with: pip install fpdf2")
        print("\nAlternative: Use online converter or the text files directly")
        return False
    
    return True

def create_readme():
    """Create README for samples"""
    readme_content = """# Sample Complaint Documents

This folder contains sample pharmaceutical customer complaint documents for testing the AIVOA complaint management system.

## Sample Files:

1. **complaint_001_contamination.txt/pdf**
   - Type: Foreign Matter Contamination
   - Severity: Critical
   - Priority: HIGH
   - Product: Amoxicillin Capsules 500mg

2. **complaint_002_discoloration.txt/pdf**
   - Type: Visual Defect - Discoloration
   - Severity: Major
   - Priority: Medium
   - Product: Ibuprofen Tablets 400mg

3. **complaint_003_packaging.txt/pdf**
   - Type: Packaging Defect - Child Resistant Closure
   - Severity: Major
   - Priority: High
   - Product: Loratadine Tablets 10mg

4. **complaint_004_labeling.txt/pdf**
   - Type: Labeling Error - Incorrect Strength
   - Severity: Critical
   - Priority: High
   - Product: Metformin HCl ER Tablets 750mg

5. **complaint_005_minor_issue.txt/pdf**
   - Type: Aesthetic/Appearance Issue
   - Severity: Minor
   - Priority: Low
   - Product: Vitamin D3 Softgels 2000 IU

## How to Use:

### Option 1: Upload PDF files
1. Run `python create_sample_pdfs.py` to convert text files to PDFs
2. Upload the generated PDF files through the web interface

### Option 2: Use text files directly
- The text files can be copied and pasted directly into the complaint processing interface

### Option 3: Online conversion
- Use any online text-to-PDF converter if you don't want to install dependencies

## Testing Different Scenarios:

- **Critical Issues**: Use complaints 001 or 004 to test HIGH priority risk assessment
- **Quality Defects**: Use complaints 001, 002, or 003 for major quality issues
- **Minor Issues**: Use complaint 005 to test LOW priority handling
- **Different Sources**: Mix of email, phone, and form-based complaints

## Expected AI Extraction:

The AI should extract:
- Customer information (name, contact)
- Product details (name, strength, batch number, dates)
- Complaint type and description
- Severity and priority levels
- Affected quantities
- Manufacturing site information

## Risk Assessment Testing:

- HIGH risk: Contamination, labeling errors
- MEDIUM risk: Discoloration, packaging defects
- LOW risk: Minor aesthetic issues
"""
    
    readme_path = Path(__file__).parent / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"\nCreated: README.md")

if __name__ == "__main__":
    print("=" * 60)
    print("AIVOA Sample Complaint Document Generator")
    print("=" * 60)
    print()
    
    # Create README
    create_readme()
    
    # Try to create PDFs
    print("\nAttempting to convert text files to PDF...")
    success = create_pdfs_simple()
    
    if not success:
        print("\n" + "=" * 60)
        print("Note: PDF conversion requires fpdf2 library")
        print("You can still use the text files for testing!")
        print("=" * 60)
