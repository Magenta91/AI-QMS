# Sample Complaint Documents - Quick Reference

## 📁 Available Files (5 Complaints)

### 1️⃣ CRITICAL - Foreign Matter Contamination
**Files**: `complaint_001_contamination.pdf/txt`

| Field | Value |
|-------|-------|
| **Product** | Amoxicillin Capsules 500mg |
| **Batch** | AMX-2024-001-A |
| **Customer** | St. Mary's Medical Center |
| **Issue** | Black foreign particles in capsules |
| **Severity** | Critical |
| **Priority** | HIGH |
| **Risk Level** | 🔴 HIGH |
| **Quantity** | 100 capsules (2 bottles) |
| **Date** | January 15, 2024 |

**Why High Risk**: Contamination with foreign matter poses direct patient safety risk, requires immediate investigation, potential FDA reportable event.

---

### 2️⃣ MAJOR - Visual Defect (Discoloration)
**Files**: `complaint_002_discoloration.pdf/txt`

| Field | Value |
|-------|-------|
| **Product** | Ibuprofen Tablets 400mg |
| **Batch** | IBU-20240110-B7 |
| **Customer** | Community Health Pharmacy Network |
| **Issue** | Yellow-brown discoloration on tablet coating |
| **Severity** | Major |
| **Priority** | Medium |
| **Risk Level** | 🟡 MEDIUM |
| **Quantity** | 200 tablets (4 bottles) |
| **Date** | January 20, 2024 |

**Why Medium Risk**: Visual defect indicating possible stability issue, product quarantined, no patient exposure yet.

---

### 3️⃣ MAJOR - Packaging Defect
**Files**: `complaint_003_packaging.pdf/txt`

| Field | Value |
|-------|-------|
| **Product** | Loratadine Tablets 10mg |
| **Batch** | LOR-2024-W15 |
| **Customer** | Central Pharmacy (Jackson Williams) |
| **Issue** | Child-resistant caps non-functional |
| **Severity** | Major |
| **Priority** | High |
| **Risk Level** | 🟡 MEDIUM |
| **Quantity** | 5 bottles (250 tablets) |
| **Date** | January 22, 2024 |
| **Source** | Email |

**Why Medium Risk**: Safety feature failure, regulatory requirement violation, but no patient harm reported.

---

### 4️⃣ CRITICAL - Labeling Error
**Files**: `complaint_004_labeling.pdf/txt`

| Field | Value |
|-------|-------|
| **Product** | Metformin HCl ER Tablets 750mg |
| **Batch** | MET-ER-750-20240118 |
| **Customer** | Riverside Hospital Pharmacy |
| **Issue** | Bottle labeled 500mg but contains 750mg tablets |
| **Severity** | Critical |
| **Priority** | High |
| **Risk Level** | 🔴 HIGH |
| **Quantity** | 30 bottles (2,700 tablets) |
| **Date** | January 25, 2024 |

**Why High Risk**: Labeling error could cause 50% overdose, serious patient safety issue, potential Class II recall, FDA violation.

---

### 5️⃣ MINOR - Cosmetic Issue
**Files**: `complaint_005_minor_issue.pdf/txt`

| Field | Value |
|-------|-------|
| **Product** | Vitamin D3 Softgels 2000 IU |
| **Batch** | VD3-2K-20240115-C |
| **Customer** | Green Valley Pharmacy (Mike Peterson) |
| **Issue** | Slightly cloudy appearance in softgels |
| **Severity** | Minor |
| **Priority** | Low |
| **Risk Level** | 🟢 LOW |
| **Quantity** | 3 bottles (180 softgels) |
| **Date** | January 28, 2024 |

**Why Low Risk**: Cosmetic variation only, no functional impact, likely natural ingredient variation, product still being sold.

---

## 🎯 Testing Strategy

### Test Case 1: High-Risk Scenario
- Use: `complaint_001_contamination.pdf` OR `complaint_004_labeling.pdf`
- Expected: Risk level HIGH, comprehensive extraction, all critical fields

### Test Case 2: Medium-Risk Scenario  
- Use: `complaint_002_discoloration.pdf` OR `complaint_003_packaging.pdf`
- Expected: Risk level MEDIUM, quality defect classification

### Test Case 3: Low-Risk Scenario
- Use: `complaint_005_minor_issue.pdf`
- Expected: Risk level LOW, informational handling

### Test Case 4: Different Formats
- All complaints have different formatting styles
- Tests AI's ability to extract from various document layouts

---

## 📊 Field Extraction Testing

Each complaint tests different extraction capabilities:

| Complaint | Customer Name | Batch | Dates | Severity | Description Length |
|-----------|---------------|-------|-------|----------|-------------------|
| 001 | ✓ Full name | ✓ | ✓ All 3 | ✓ Critical | Long |
| 002 | ✓ Organization | ✓ | ✓ All 3 | ✓ Major | Very Long |
| 003 | ✓ From email | ✓ | ✓ 2 of 3 | ✓ Major | Medium |
| 004 | ✓ Hospital | ✓ | ✓ All 3 | ✓ Critical | Very Long |
| 005 | ✓ Pharmacy | ✓ | ✓ All 3 | ✓ Minor | Short |

---

## 🚀 Quick Test Commands

### Test PDF Upload (Windows PowerShell)
```powershell
# Navigate to samples folder
cd samples

# Test with critical complaint
curl.exe -X POST "http://127.0.0.1:8000/api/complaints/upload" `
  -F "file=@complaint_001_contamination.pdf"
```

### Test with All Samples
```powershell
# Upload and test each sample
$samples = @(
    "complaint_001_contamination.pdf",
    "complaint_002_discoloration.pdf",
    "complaint_003_packaging.pdf",
    "complaint_004_labeling.pdf",
    "complaint_005_minor_issue.pdf"
)

foreach ($sample in $samples) {
    Write-Host "Testing: $sample"
    curl.exe -X POST "http://127.0.0.1:8000/api/complaints/upload" -F "file=@$sample"
    Start-Sleep -Seconds 2
}
```

---

## ✅ Expected Results Summary

| Sample | Extraction Quality | Risk Level | Completeness | Processing Time |
|--------|-------------------|------------|--------------|-----------------|
| 001 | Excellent (90%+) | HIGH 🔴 | 85-95% | 10-20s |
| 002 | Excellent (90%+) | MEDIUM 🟡 | 85-95% | 10-20s |
| 003 | Good (80%+) | MEDIUM 🟡 | 75-85% | 10-20s |
| 004 | Excellent (90%+) | HIGH 🔴 | 90-95% | 10-20s |
| 005 | Good (75%+) | LOW 🟢 | 70-80% | 10-20s |

---

## 📋 Checklist for Each Test

For every sample you test, verify:

- [ ] PDF uploads without errors
- [ ] Text extraction completes
- [ ] AI extracts product name
- [ ] AI extracts batch number
- [ ] AI extracts customer name
- [ ] AI extracts dates (mfg, exp, complaint)
- [ ] AI extracts complaint description
- [ ] AI assigns severity level correctly
- [ ] Risk assessment appears
- [ ] Risk level matches expected (HIGH/MEDIUM/LOW)
- [ ] Risk reasons are relevant
- [ ] Completeness percentage calculated
- [ ] Form fields are editable after extraction
- [ ] UI shows processing status
- [ ] Total time under 30 seconds

---

## 🎓 Learning Points

These samples demonstrate:

1. **Variety in format**: Email vs form vs structured report
2. **Different risk levels**: Critical, major, minor issues
3. **Extraction complexity**: From simple to complex documents
4. **Real-world scenarios**: Actual pharmaceutical quality issues
5. **Regulatory considerations**: FDA requirements, recalls, CAPA

---

## 💡 Tips

1. **Start simple**: Begin with complaint_005 (shortest, simplest)
2. **Test variety**: Try all 5 to see AI handling different formats
3. **Check logs**: Backend logs show detailed AI processing steps
4. **Compare results**: See if risk levels match your assessment
5. **Edit after extraction**: Test manual field correction

---

## 📝 Notes

- All samples are realistic pharmaceutical complaints
- Product names and batch numbers are fictional
- Customer names are fictional
- Issues described are common in pharma industry
- Regulatory references are accurate
- Can be used for interview demonstrations
