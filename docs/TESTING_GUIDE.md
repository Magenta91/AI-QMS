# AIVOA Complaint System - Testing Guide

## Quick Start

1. **Open the application**: Navigate to http://localhost:5173
2. **Upload a sample complaint**: Click "Choose File" in the AI Copilot panel
3. **Watch the magic happen**: See AI extract and populate the form automatically

## Sample Documents Location

All sample complaint documents are in the `/samples` folder:

```
samples/
├── complaint_001_contamination.pdf     (Critical - Foreign Matter)
├── complaint_002_discoloration.pdf     (Major - Visual Defect)
├── complaint_003_packaging.pdf         (Major - Child-Resistant Cap)
├── complaint_004_labeling.pdf          (Critical - Wrong Strength Label)
├── complaint_005_minor_issue.pdf       (Minor - Cosmetic Issue)
└── README.md                           (Detailed descriptions)
```

## Testing Workflow

### Test 1: Critical Contamination Case
**File**: `complaint_001_contamination.pdf`

**What to expect**:
- Product: Amoxicillin Capsules 500mg
- Risk Level: HIGH
- All critical fields populated
- Batch number: AMX-2024-001-A
- Customer: St. Mary's Medical Center

### Test 2: Visual Defect Case
**File**: `complaint_002_discoloration.pdf`

**What to expect**:
- Product: Ibuprofen Tablets 400mg
- Risk Level: MEDIUM
- Priority: Medium
- Batch: IBU-20240110-B7
- Customer: Community Health Pharmacy Network

### Test 3: Packaging Defect
**File**: `complaint_003_packaging.pdf`

**What to expect**:
- Email-formatted complaint
- Product: Loratadine Tablets 10mg
- Child-resistant cap failure
- Should extract customer name from email

### Test 4: Labeling Error (Most Critical)
**File**: `complaint_004_labeling.pdf`

**What to expect**:
- Product: Metformin HCl ER 750mg
- Risk Level: HIGH
- Wrong strength on label (critical patient safety issue)
- Detailed regulatory impact section
- Customer: Riverside Hospital Pharmacy

### Test 5: Minor Aesthetic Issue
**File**: `complaint_005_minor_issue.pdf`

**What to expect**:
- Product: Vitamin D3 Softgels 2000 IU
- Risk Level: LOW
- Priority: Low
- Cosmetic appearance issue only

## What the AI Should Extract

For each complaint, the system should extract:

✓ **Customer Information**
- Customer name
- Contact person (if different)
- Complaint source (Email/Phone/Form)

✓ **Product Details**
- Product name
- Product strength/grade
- Batch/Lot number
- Manufacturing date
- Expiry date
- Quantity affected
- Manufacturing site

✓ **Complaint Details**
- Complaint type
- Complaint description (full narrative)
- Initial severity (Critical/Major/Minor)
- Priority (High/Medium/Low)
- Date received

## Expected AI Behavior

### Extraction Process (10-20 seconds)
1. Upload PDF → "Uploading..."
2. Extract text → "Extracted X characters..."
3. AI processing → "Processing through AI workflow..."
4. Form population → Fields auto-fill
5. Risk assessment → Colored risk badge appears

### Risk Assessment Output
The AI should provide:
- **Risk Level**: HIGH / MEDIUM / LOW (color-coded)
- **Reasons**: 2-3 specific reasons for the risk level
- **Recommended Action**: Next steps for QA team
- **Disclaimer**: Reminder that human review is required

### Completeness Check
The system calculates completeness as:
```
Completeness = (Fields Populated / Total Fields) × 100%
```

Expected ranges:
- Good complaints: 70-90%
- Excellent complaints: 90%+
- Missing info: <70%

## Testing Scenarios

### Scenario 1: Full Workflow Test
1. Upload `complaint_001_contamination.pdf`
2. Verify all fields populate correctly
3. Check risk assessment shows HIGH
4. Verify completeness percentage
5. Manually correct a field
6. Save the complaint

### Scenario 2: Different Risk Levels
1. Upload critical case (001 or 004) → Should show HIGH risk
2. Upload major case (002 or 003) → Should show MEDIUM risk
3. Upload minor case (005) → Should show LOW risk

### Scenario 3: Validation Test
1. Upload a complaint
2. Clear a required field (e.g., batch_number)
3. System should show validation error
4. Missing fields should be highlighted

### Scenario 4: Multiple Uploads
1. Upload complaint 001
2. Review extracted data
3. Upload complaint 002
4. Verify previous data is replaced
5. Form should show new complaint data

## API Endpoints for Manual Testing

### Health Check
```bash
curl http://127.0.0.1:8000/health
```

### Upload Document
```bash
curl -X POST "http://127.0.0.1:8000/api/complaints/upload" \
  -F "file=@samples/complaint_001_contamination.pdf"
```

### Process Text Directly
```bash
curl -X POST "http://127.0.0.1:8000/api/complaints/process" \
  -H "Content-Type: application/json" \
  -d '{"text":"Customer reported contamination in Amoxicillin batch AMX-001...","source_type":"text"}'
```

### Risk Assessment
```bash
curl -X POST "http://127.0.0.1:8000/api/risk/assess" \
  -H "Content-Type: application/json" \
  -d '{"product_name":"Amoxicillin","complaint_description":"Foreign particles found","complaint_type":"contamination"}'
```

## Troubleshooting

### Problem: Upload button doesn't work
- Check browser console for errors
- Verify backend is running on port 8000
- Check CORS settings

### Problem: AI extraction fails
- Verify Groq API key in backend/.env
- Check backend logs for errors
- Try with smaller/simpler PDF

### Problem: Risk assessment not appearing
- Wait for full workflow completion
- Check network tab for failed API calls
- Verify risk service is working

### Problem: Form fields not populating
- Check Redux DevTools (if installed)
- Verify complaint data in copilot messages
- Look for JavaScript errors in console

## Backend Logs

The backend provides detailed logging:

```
INFO:aivoa.API | Received file upload: complaint_001.pdf
INFO:aivoa.LANGGRAPH | Running extraction node
INFO:aivoa.GROQ | Calling Groq API with model gemma2-9b-it
INFO:aivoa.LANGGRAPH | Successfully extracted 12 fields
INFO:aivoa.LANGGRAPH | Running validation node
INFO:aivoa.LANGGRAPH | Running completeness check node
INFO:aivoa.LANGGRAPH | Completeness: 85.7% (12/14 fields)
INFO:aivoa.LANGGRAPH | Running risk assessment node
INFO:aivoa.RISK | Performing AI risk assessment
```

## Performance Expectations

- **PDF Upload**: < 2 seconds
- **Text Extraction**: < 1 second
- **AI Processing**: 5-15 seconds (depends on Groq API)
- **Risk Assessment**: 3-8 seconds
- **Total Time**: 10-25 seconds end-to-end

## Success Criteria

✓ PDF uploads successfully  
✓ Text extraction works  
✓ AI extracts at least 70% of fields correctly  
✓ Risk assessment provides reasonable output  
✓ Form is editable after extraction  
✓ UI remains responsive during processing  
✓ Error messages are clear and helpful  

## Known Limitations (MVP)

- Only PDF files supported (no DOCX, images)
- No OCR for scanned documents
- No database persistence yet (mock save)
- No duplicate detection yet
- Simple rule-based completeness (no AI)
- English language only

## Next Steps After Testing

1. Implement database persistence
2. Add duplicate detection
3. Add conversational correction via chat
4. Support more file formats
5. Add batch processing
6. Implement CAPA recommendations
7. Add report generation

## Support

If you encounter issues:
1. Check backend terminal for detailed logs
2. Check browser console for frontend errors
3. Verify all services are running
4. Try with different sample files
5. Check the API documentation at http://127.0.0.1:8000/docs
