# OCR API Test Suite - Reference Card

## 📌 Essential Commands

```bash
# Start API server (Terminal 1)
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Run all tests (Terminal 2)
cd backend
.venv\Scripts\activate
pytest tests/test_phocr_output.py -v

# Run with output
pytest tests/test_phocr_output.py -v -s

# Run specific test category
pytest tests/test_phocr_output.py::TestExtractionAPI -v      # Extraction only
pytest tests/test_phocr_output.py::TestVerificationAPI -v    # Verification only
pytest tests/test_phocr_output.py::TestAPIEdgeCases -v       # Edge cases only

# Run specific image tests
pytest tests/test_phocr_output.py -k "1.png" -v

# Install dependencies
pip install pytest pytest-timeout requests
```

---

## 📂 File Locations

```
backend/tests/
├── test_phocr_output.py     ← Main test file (EDIT EXPECTED_OUTPUTS here)
├── conftest.py              ← Configuration (usually don't edit)
├── README.md                ← Full documentation
├── QUICK_START.md           ← Quick reference
├── INDEX.md                 ← Navigation guide
└── Results/
    ├── 1.png               ← Test images
    ├── 2.png
    └── 3.png
```

---

## 🎯 Test Locations in Code

### Extraction Tests
**File:** `test_phocr_output.py` lines 57-161
- `test_extraction_consistency` - Run 5 times per image
- `test_extraction_with_detection_overlay` - Check overlay functionality

### Verification Tests
**File:** `test_phocr_output.py` lines 164-250
- `test_verification_consistency` - Run 5 times per image
- `test_verification_field_results` - Check field details

### Edge Cases
**File:** `test_phocr_output.py` lines 253-310
- `test_extraction_missing_file` - Missing file handling
- `test_extraction_invalid_json_fields` - Invalid JSON handling
- `test_verification_empty_verification_data` - Empty data handling

---

## 🔧 Configuration

### Expected Output Values
**File:** `test_phocr_output.py` lines 13-51

```python
EXPECTED_OUTPUTS = {
    "1.png": {
        "fields": ["name", "date of birth", "gender", "aadhaar number"],
        "expected_mapped_fields": {
            "name": "vaishnavi singh",              # ← Edit these
            "date of birth": "16/11/2004",
            # ...
        },
        "verification_data": {
            "name": "vaishnavi singh",              # ← And these
            # ...
        },
    },
}
```

### Similarity Threshold
**File:** `test_phocr_output.py` line ~380

```python
def is_similar(str1, str2, threshold=0.75):  # ← Change to 0.5-0.9
```

---

## ✅ Test Pass/Fail Criteria

| Scenario | Result | Status |
|----------|--------|--------|
| 5/5 iterations match | PASS | ✅ |
| 4/5 iterations match | PASS | ✅ |
| 3/5 iterations match | PASS | ✅ |
| 2/5 iterations match | FAIL | ❌ |
| 1/5 iterations match | FAIL | ❌ |
| 0/5 iterations match | FAIL | ❌ |

**Minimum:** > 3 out of 5 (60% success rate)

---

## 🚀 Full Test Sequence

```
1. Start API Server
   ↓
2. Open new terminal
   ↓
3. Activate venv (.venv\Scripts\activate)
   ↓
4. Run pytest (pytest tests/test_phocr_output.py -v)
   ↓
5. View results (check console output)
   ↓
6. If failed: Debug and update EXPECTED_OUTPUTS
   ↓
7. Rerun tests
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Server not running" | Run: `uvicorn app.main:app --reload` |
| "Test image not found" | Check: `ls backend/tests/Results/` |
| "ModuleNotFoundError: pytest" | Run: `pip install pytest requests` |
| "Port 8000 in use" | Change port: `--port 8001` |
| "< 3/5 iterations match" | Update `EXPECTED_OUTPUTS` values |
| "Connection refused" | Ensure API server is running |

---

## 📊 Understanding Test Output

### ✅ Passing Output
```
test_extraction_consistency[1.png] PASSED
1.png - Extraction API: 4/5 iterations matched expected output
```
**Meaning:** Test passed, 4 out of 5 runs matched

### ❌ Failing Output
```
test_extraction_consistency[1.png] FAILED
Extraction test failed for 1.png: Only 2/5 iterations matched (need > 3)
```
**Meaning:** Test failed, only 2 out of 5 runs matched (need > 3)

---

## 🔄 Test API Endpoints

### Extraction API
```
POST /extract
Content-Type: multipart/form-data

Body:
- document: (file) image file
- include_detection: "true" or "false"
- fields: ["field1", "field2", ...]

Response:
{
  "mapped_fields": {...},
  "detections": [...],
  "processing_info": {...},
  "confidence_overlay": "base64_string",
  "has_detection_data": true
}
```

### Verification API
```
POST /verify
Content-Type: multipart/form-data

Body:
- document: (file) image file
- verification_data: {"field": "value", ...}
- fields: ["field1", "field2", ...]

Response:
{
  "success": true,
  "verification_result": {
    "overall_status": "verified",
    "overall_confidence": 95,
    "field_results": {...}
  }
}
```

---

## 📈 Test Coverage

| Category | Tests | Images | Iterations | Total Runs |
|----------|-------|--------|------------|-----------|
| Extraction | 2 | 3 | 5 | 30+ |
| Verification | 2 | 3 | 5 | 30+ |
| Edge Cases | 3 | - | 1 | 3 |
| **Total** | **7** | **3** | **~** | **~60+** |

---

## 🎓 Key Concepts

### Why 5 Iterations?
ML outputs vary. 5 runs account for variance and validate consistency.

### Why >3 Match?
- 3-5 matches = 60-100% success = API working well
- <3 matches = <60% success = Real problems

### Fuzzy Matching?
Handles: case differences, minor typos, OCR variations

### Parametrization?
`@pytest.mark.parametrize()` generates tests automatically:
```python
@pytest.mark.parametrize("image_name", ["1.png", "2.png", "3.png"])
def test_extraction_consistency(self, image_name):
    # Automatically runs 3 times with different images
```

---

## 📖 Documentation Map

```
START HERE → QUICK_START.md (5 min)
     ↓
Get full info → README.md (15 min)
     ↓
Understand tech → IMPLEMENTATION_SUMMARY.md (10 min)
     ↓
Navigate files → INDEX.md (5 min)
     ↓
Quick ref → This file (2 min)
```

---

## ⚡ Most Common Commands

```bash
# Setup (one time)
cd backend
pip install pytest pytest-timeout requests
.venv\Scripts\activate

# Run tests
pytest tests/test_phocr_output.py -v

# Run with details
pytest tests/test_phocr_output.py -vv -s

# Run one test category
pytest tests/test_phocr_output.py::TestExtractionAPI -v

# Update and rerun
# 1. Edit EXPECTED_OUTPUTS in test_phocr_output.py
# 2. pytest tests/test_phocr_output.py -v

# Debugging
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] -vv -s
```

---

## 🔐 Important Paths

| Item | Path |
|------|------|
| Test file | `backend/tests/test_phocr_output.py` |
| Config | `backend/tests/conftest.py` |
| Images | `backend/tests/Results/` |
| Docs | `backend/tests/README.md` |
| API | `http://127.0.0.1:8000` |

---

## ✨ Quick Edit Checklist

```
To customize tests:

[ ] Update EXPECTED_OUTPUTS in test_phocr_output.py
[ ] Run: pytest tests/test_phocr_output.py -v
[ ] Review test output
[ ] Adjust values if needed
[ ] Rerun tests
[ ] Verify > 3/5 pass rate
```

---

## 🎯 Success Criteria

✅ Test is PASSING when:
- More than 3 out of 5 iterations match expected output
- Response has correct structure
- No connection errors
- API returns 200 status code

❌ Test is FAILING when:
- Less than 3 out of 5 iterations match
- API returns error status code
- Response is malformed
- Connection refused/timeout

---

## 📞 Quick Help

**Need quick start?** → QUICK_START.md
**Need full docs?** → README.md
**Need tech details?** → IMPLEMENTATION_SUMMARY.md
**Need navigation?** → INDEX.md
**Need quick ref?** → This file

---

**Keep this card handy for quick reference!**

Last updated: December 2025
