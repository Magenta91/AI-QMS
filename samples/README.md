# Sample Complaint Documents

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
