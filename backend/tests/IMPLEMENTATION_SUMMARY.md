# OCR API Test Suite - Implementation Summary

## Overview

A comprehensive test suite has been created for testing the Multilingual OCR Extraction & Verification API. The suite is designed specifically for ML-based systems where outputs can vary between runs.

## Files Created

### 1. `test_phocr_output.py` (Main Test Suite)
**Location:** `backend/tests/test_phocr_output.py`

**Contains:**
- `TestExtractionAPI` class with extraction endpoint tests
- `TestVerificationAPI` class with verification endpoint tests  
- `TestAPIEdgeCases` class with error handling tests
- Utility function `is_similar()` for fuzzy string matching

**Key Features:**
- Tests each image 5 times to account for ML model variance
- Passes test if output matches expected values more than 3 times out of 5
- Tests both extraction and verification APIs
- Validates response structure and data types
- Includes detection overlay functionality testing

### 2. `conftest.py` (Pytest Configuration)
**Location:** `backend/tests/conftest.py`

**Contains:**
- API server availability check
- Test fixtures for image paths
- Session-level configuration
- Automatic server validation before running tests

### 3. `README.md` (Test Documentation)
**Location:** `backend/tests/README.md`

**Contains:**
- Installation instructions
- How to run tests
- Test case descriptions
- Debugging guide
- Expected test results
- CI/CD integration examples

## Test Design Rationale

### Why 5 Iterations?
Machine learning models produce variable outputs. By running each test 5 times:
- We reduce false positives/negatives
- We verify consistency rather than perfection
- We can tolerate 1-2 failures due to model variance

### Why >3 Match Threshold?
- 4-5 matches = consistent, reliable extraction
- 3 matches = borderline, potential issues
- <3 matches = likely real problems

## Test Cases

### Extraction API Tests

#### Test 1: `test_extraction_consistency` (Parametrized)
```
Test each image (1.png, 2.png, 3.png) with extraction API 5 times
├─ Send POST request to /extract endpoint
├─ Validate response structure (mapped_fields, detections, processing_info)
├─ Compare extracted fields with expected output (case-insensitive, fuzzy matching)
└─ Pass if > 3 matches out of 5
```

#### Test 2: `test_extraction_with_detection_overlay`
```
Test extraction with confidence overlay enabled for image 1.png
├─ Send request with include_detection=true
├─ Validate confidence_overlay field contains base64 image
└─ Verify has_detection_data is True
```

### Verification API Tests

#### Test 3: `test_verification_consistency` (Parametrized)
```
Test each image (1.png, 2.png, 3.png) with verification API 5 times
├─ Send POST request to /verify endpoint with verification data
├─ Validate response structure (success, verification_result)
├─ Check overall_status field
└─ Pass if > 3 successful responses out of 5
```

#### Test 4: `test_verification_field_results`
```
Test detailed field-level verification results for image 1.png
├─ Verify field_results contains all submitted fields
├─ Check each field has: submitted_value, extracted_value, similarity_score, status, confidence
└─ Validate all expected keys are present
```

### Edge Case Tests

#### Test 5: `test_extraction_missing_file`
```
Test API behavior with missing document file
├─ Send request without document
└─ Expect non-200 status code (error handling)
```

#### Test 6: `test_extraction_invalid_json_fields`
```
Test API behavior with malformed JSON fields parameter
├─ Send request with invalid JSON
└─ Expect non-200 status code (validation)
```

#### Test 7: `test_verification_empty_verification_data`
```
Test API behavior with empty verification data
├─ Send request with {} as verification_data
└─ Expect 200 response (graceful handling)
```

## Key Features

### 1. Fuzzy String Matching
```python
def is_similar(str1, str2, threshold=0.75):
    # Handles:
    # - Case insensitivity
    # - Partial matches
    # - Minor OCR errors (character substitutions)
```

### 2. Parametrized Testing
```python
@pytest.mark.parametrize("image_name", ["1.png", "2.png", "3.png"])
# Runs test once for each image automatically
```

### 3. Automatic Server Validation
```python
# conftest.py automatically checks if API is running
# Fails test session if server unavailable
```

### 4. Detailed Test Output
```
1.png - Extraction API: 4/5 iterations matched expected output
2.png - Verification API: 5/5 iterations succeeded
```

## Expected Outputs Configuration

Edit `EXPECTED_OUTPUTS` in `test_phocr_output.py`:

```python
EXPECTED_OUTPUTS = {
    "image_name.png": {
        "fields": ["field1", "field2"],
        "expected_mapped_fields": {
            "field1": "expected_value",
            "field2": "expected_value",
        },
        "verification_data": {
            "field1": "expected_value",
            "field2": "expected_value",
        },
    },
}
```

## Running the Tests

### Quick Start
```bash
# Terminal 1: Start API server
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Run tests
cd backend
.venv\Scripts\activate
pytest tests/test_phocr_output.py -v
```

### Advanced Options
```bash
# Verbose output with print statements
pytest tests/test_phocr_output.py -vv -s

# Run specific test class
pytest tests/test_phocr_output.py::TestExtractionAPI -v

# Run specific image tests
pytest tests/test_phocr_output.py -k "1.png" -v

# Set timeout for long-running tests
pytest tests/test_phocr_output.py --timeout=60
```

## Test Results Interpretation

### ✅ Test Passes
```
test_extraction_consistency[1.png] PASSED
1.png - Extraction API: 4/5 iterations matched expected output
```
Meaning: The API consistently extracts the expected fields

### ❌ Test Fails
```
test_extraction_consistency[1.png] FAILED
Extraction test failed for 1.png: Only 2/5 iterations matched expected output
```
Meaning: The API is not reliably extracting expected fields

## Dependencies

Required packages:
```
pytest>=7.0.0
pytest-timeout>=2.1.0
requests>=2.28.0
```

Install with:
```bash
pip install pytest pytest-timeout requests
```

## Extensibility

### Adding New Test Images
1. Place image in `backend/tests/Results/new_image.png`
2. Add to `EXPECTED_OUTPUTS`:
   ```python
   "new_image.png": {
       "fields": [...],
       "expected_mapped_fields": {...},
       "verification_data": {...},
   }
   ```
3. Tests automatically run for new image (parametrized)

### Customizing Similarity Threshold
```python
# In is_similar() function
return similarity >= threshold  # Change 0.75 to desired value
```

### Adding Custom Assertions
```python
def test_custom_extraction():
    # Add custom logic
    assert response.get("mapped_fields").get("field") == "value"
```

## Performance Expectations

- Per image: ~1-3 minutes (5 iterations × 2 endpoints)
- Full suite: ~5-15 minutes
- Adjustable via `--timeout` flag

## Continuous Integration

Ready for CI/CD:
- GitHub Actions example in README.md
- Automated server health check
- Clear pass/fail criteria
- Detailed error messages

## Troubleshooting

### Common Issues

**"API server is not running"**
- Start server: `uvicorn app.main:app --reload`

**"Test image not found"**
- Check images exist in `backend/tests/Results/`

**"ModuleNotFoundError"**
- Install dependencies: `pip install pytest requests`

**"Tests fail inconsistently"**
- This is expected with ML models
- Adjust expected values or similarity threshold

## Future Enhancements

Potential additions:
- Performance benchmarking
- Confidence score validation
- PDF multi-page testing
- Language detection validation
- Integration with CI/CD pipelines
- Test result reporting/dashboards
