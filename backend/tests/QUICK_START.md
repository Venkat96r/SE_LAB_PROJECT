# Quick Start Guide - OCR API Tests

## One-Minute Setup

### Step 1: Install Dependencies (1 minute)
```bash
cd backend
pip install pytest pytest-timeout requests
```

### Step 2: Start API Server (Terminal 1)
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Wait for: `INFO: Uvicorn running on http://127.0.0.1:8000`

### Step 3: Run Tests (Terminal 2)
```bash
cd backend
.venv\Scripts\activate
pytest tests/test_phocr_output.py -v
```

## Expected Output

```
tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] PASSED
1.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[2.png] PASSED
2.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[3.png] PASSED
3.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestVerificationAPI::test_verification_consistency[1.png] PASSED
1.png - Verification API: 5/5 iterations succeeded

... (more tests)
```

## Common Commands

```bash
# Run all tests with verbose output
pytest tests/test_phocr_output.py -v

# Run only extraction tests
pytest tests/test_phocr_output.py::TestExtractionAPI -v

# Run only verification tests
pytest tests/test_phocr_output.py::TestVerificationAPI -v

# Run tests for specific image
pytest tests/test_phocr_output.py -k "1.png" -v

# Show all print output
pytest tests/test_phocr_output.py -v -s

# Set timeout (for slow systems)
pytest tests/test_phocr_output.py -v --timeout=60

# Run single test with debugging
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_with_detection_overlay -v -s
```

## Test Overview

**Total Tests:** 7 (but parametrized = 9 actual test runs)
- 3 × Extraction Consistency (1 per image)
- 2 × Extraction Other (overlay, structure)
- 3 × Verification Consistency (1 per image)  
- 2 × Verification Other (field results, structure)
- 3 × Edge Cases

**Runtime:** ~5-15 minutes total
- Each test makes 5 API calls
- ML processing can be slow

## What Each Test Does

### Extraction Tests
✅ Sends image to `/extract` endpoint
✅ Checks if extracted fields match expected values
✅ Runs 5 times per image
✅ **Passes if > 3 match** out of 5

### Verification Tests
✅ Sends image + expected data to `/verify` endpoint
✅ Validates verification results
✅ Checks field-level comparison data
✅ **Passes if > 3 succeed** out of 5

### Edge Case Tests
✅ Tests error handling
✅ Validates API robustness
✅ Checks edge cases

## If Tests Fail

### Issue: "API server is not running"
```bash
# In Terminal 1:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Issue: "Test image not found"
```bash
# Check images exist:
ls backend/tests/Results/
# Should show: 1.png  2.png  3.png
```

### Issue: "ModuleNotFoundError: pytest"
```bash
pip install pytest pytest-timeout requests
```

### Issue: "Only 2/5 iterations matched"
This can happen if:
- Expected values don't match your images
- ML model is performing poorly
- Update `EXPECTED_OUTPUTS` in `test_phocr_output.py`

## Customizing Tests

Edit `test_phocr_output.py`:

```python
EXPECTED_OUTPUTS = {
    "1.png": {
        "fields": ["your", "fields", "here"],  # Change this
        "expected_mapped_fields": {
            "your": "expected_value",  # Change this
            "fields": "expected_value",
            "here": "expected_value",
        },
        "verification_data": {
            "your": "expected_value",  # Change this
            "fields": "expected_value",
            "here": "expected_value",
        },
    },
}
```

## Viewing Detailed Results

```bash
# See all extracted values and comparison results
pytest tests/test_phocr_output.py -vv -s

# Get full error messages
pytest tests/test_phocr_output.py -vv --tb=short

# Show only failed tests with details
pytest tests/test_phocr_output.py -vv --tb=long -x
```

## File Structure

```
backend/
├── tests/
│   ├── test_phocr_output.py      ← Main test file
│   ├── conftest.py               ← Pytest configuration
│   ├── README.md                 ← Full documentation
│   ├── IMPLEMENTATION_SUMMARY.md ← This file
│   └── Results/
│       ├── 1.png                 ← Test image 1
│       ├── 2.png                 ← Test image 2
│       └── 3.png                 ← Test image 3
├── app/
├── requirements.txt
└── ...
```

## Test Passing Criteria

✅ **PASS** - More than 3 out of 5 iterations match
```
1.png - Extraction API: 4/5 iterations matched expected output
```

❌ **FAIL** - 3 or fewer iterations match
```
Only 2/5 iterations matched expected output (need > 3)
```

## Next Steps

1. **Run basic test:**
   ```bash
   pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency -v -s
   ```

2. **Update expected values** based on actual output

3. **Run full suite** when ready:
   ```bash
   pytest tests/test_phocr_output.py -v
   ```

4. **Integrate with CI/CD** (see README.md for examples)

---

**Questions?** Check README.md for detailed documentation.
