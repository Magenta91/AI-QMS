# 🚀 AIVOA Complaint System - Quick Start

## ✅ System Status: READY

All services are running and configured with working models!

---

## 🎯 Start Using the System (3 Steps)

### Step 1: Open the Application
Navigate to: **http://localhost:5173**

### Step 2: Upload a Sample Document
1. Click the **"Choose File"** button in the AI Copilot panel
2. Navigate to the `samples` folder
3. Select any `.pdf` file (start with `complaint_005_minor_issue.pdf` - it's the simplest)
4. Click "Open"

### Step 3: Watch the AI Work
- Upload progress shows in the copilot panel
- Wait 10-20 seconds for processing
- Form automatically populates with extracted data
- Risk assessment appears on the right side

**That's it!** 🎉

---

## 📋 Sample Files (Ready to Test)

All in the `samples/` folder:

| File | Risk Level | Complexity | Processing Time |
|------|------------|------------|-----------------|
| `complaint_005_minor_issue.pdf` | 🟢 LOW | Easy | ~10s |
| `complaint_002_discoloration.pdf` | 🟡 MEDIUM | Medium | ~15s |
| `complaint_003_packaging.pdf` | 🟡 MEDIUM | Medium | ~15s |
| `complaint_001_contamination.pdf` | 🔴 HIGH | Hard | ~20s |
| `complaint_004_labeling.pdf` | 🔴 HIGH | Hard | ~20s |

**Tip**: Start with #5 (minor issue) for quickest results!

---

## 🔧 Current Configuration

### ✅ Running Services

- **PostgreSQL**: localhost:5432 (Docker)
- **Backend API**: http://127.0.0.1:8000
- **Frontend**: http://localhost:5173

### ✅ AI Model

- **Model**: `openai/gpt-oss-120b`
- **Provider**: Groq
- **Speed**: 500 tokens/second
- **Quality**: Excellent (120B parameters)
- **Status**: Verified working

### ✅ Features Available

- ✅ PDF document upload
- ✅ AI text extraction
- ✅ Structured data extraction (15+ fields)
- ✅ Field validation
- ✅ Completeness checking
- ✅ AI risk assessment
- ✅ Manual field editing
- ✅ Real-time status updates

---

## 🎓 What to Expect

### When You Upload a Document:

1. **Uploading...** (2 seconds)
   - PDF uploads to backend
   - Text extracted using pypdf

2. **Extracting...** (5-10 seconds)
   - AI analyzes the complaint text
   - Structured data extracted

3. **Processing...** (3-5 seconds)
   - Validation runs
   - Completeness calculated
   - Risk assessment performed

4. **Complete!** (instant)
   - Form populates with data
   - Risk level displayed
   - Completeness percentage shown

**Total Time**: 10-20 seconds

### Expected Results:

#### Form Fields Auto-Populated:
- Customer Name
- Product Name & Strength
- Batch Number
- Manufacturing & Expiry Dates
- Complaint Type & Description
- Severity & Priority
- And more...

#### Risk Assessment Shows:
- Risk Level (HIGH 🔴 / MEDIUM 🟡 / LOW 🟢)
- 2-3 reasons for the risk level
- Recommended action
- Disclaimer about human review

#### Completeness Score:
- Percentage of fields filled
- List of missing fields
- Validation errors (if any)

---

## 🧪 Quick Test

Want to verify everything works? Run this:

```powershell
# Test backend health
curl http://127.0.0.1:8000/health

# Expected: {"status":"ok","service":"aivoa-backend"}
```

Or test with a sample file:

```powershell
cd samples
curl -X POST "http://127.0.0.1:8000/api/complaints/upload" `
  -F "file=@complaint_005_minor_issue.pdf"
```

---

## 📊 System Performance

Typical performance with current setup:

| Operation | Time | Status |
|-----------|------|--------|
| PDF Upload | < 2s | ✅ |
| Text Extraction | < 1s | ✅ |
| AI Extraction | 5-10s | ✅ |
| Risk Assessment | 3-6s | ✅ |
| **Total** | **10-20s** | ✅ |

---

## 🐛 Troubleshooting

### Problem: Upload button doesn't respond
**Solution**: Refresh the page (http://localhost:5173)

### Problem: "Processing..." never completes
**Solution**: 
1. Check backend is running: `curl http://127.0.0.1:8000/health`
2. Check browser console for errors (F12)
3. Try a smaller file (complaint_005)

### Problem: No risk assessment appears
**Solution**: 
1. Wait a bit longer (up to 30 seconds)
2. Check backend logs for errors
3. Verify Groq API key in `.env`

### Problem: Form doesn't populate
**Solution**:
1. Check if extraction succeeded (look at copilot messages)
2. Check browser console for JavaScript errors
3. Verify Redux state in DevTools

---

## 📖 Documentation

Need more details? Check these files:

- **TESTING_GUIDE.md** - Comprehensive testing instructions
- **MODEL_UPDATE.md** - AI model information
- **SYSTEM_STATUS.md** - Full system overview
- **samples/SAMPLES_INFO.md** - Sample document details
- **samples/README.md** - Sample descriptions

---

## 🎯 Next Actions

### For Testing:
1. Upload each sample document
2. Verify extraction accuracy
3. Check risk assessment reasonableness
4. Test manual field editing
5. Try correcting a field

### For Development:
1. Review code in `backend/app/`
2. Understand LangGraph workflow
3. Examine AI prompts
4. Test API endpoints directly
5. Add new features

### For Demo:
1. Prepare walkthrough script
2. Practice the upload workflow
3. Explain the AI extraction process
4. Show risk assessment logic
5. Discuss architecture decisions

---

## 💡 Pro Tips

1. **Fastest test**: Use `complaint_005_minor_issue.pdf` (~10 seconds)
2. **Best showcase**: Use `complaint_004_labeling.pdf` (most detailed)
3. **Clear cache**: Refresh page if something seems stuck
4. **Check logs**: Backend terminal shows detailed processing steps
5. **API docs**: Visit http://127.0.0.1:8000/docs for Swagger UI

---

## ✅ Pre-Launch Checklist

Before demo or presentation:

- [ ] All services running (`docker ps`, check terminals)
- [ ] Health endpoint responding (`curl http://127.0.0.1:8000/health`)
- [ ] Frontend loads (`http://localhost:5173`)
- [ ] Sample PDFs ready in `samples/` folder
- [ ] Backend logs visible (optional, for debugging)
- [ ] Browser window ready with UI open
- [ ] Know which sample to demo first

---

## 🎉 You're All Set!

The system is **fully operational** and ready to use.

**Start here**: http://localhost:5173

**Test file**: `samples/complaint_005_minor_issue.pdf`

**Total time to first result**: < 15 seconds

---

**Questions?** Check:
- TESTING_GUIDE.md for detailed instructions
- MODEL_UPDATE.md for AI model info
- SYSTEM_STATUS.md for technical details

**Happy testing!** 🚀
