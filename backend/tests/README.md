# OCR API Test Suite

## Overview

This test suite provides comprehensive testing for the Multilingual OCR Extraction & Verification API. The tests are designed to handle the variability of machine learning outputs by running each test 5 times and checking for consistency.

## Test Structure

### Test Files
- **`test_phocr_output.py`** - Main test suite with extraction and verification API tests
- **`conftest.py`** - Pytest configuration and fixtures
- **`Results/`** - Directory containing test images (1.png, 2.png, 3.png)

## Requirements

### Prerequisites
- Python 3.8+
- Backend API running on `http://127.0.0.1:8000`
- Test images in `backend/tests/Results/` directory

### Required Packages
```bash
pytest>=7.0.0
pytest-timeout>=2.1.0
requests>=2.28.0
```

## Installation

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Activate virtual environment:**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install test dependencies:**
```bash
pip install pytest pytest-timeout requests
```

## Running the Tests

### Start the API Server

In one terminal, start the backend server:

```bash
# From backend directory with venv activated
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Run Tests in Another Terminal

```bash
# From backend directory with venv activated
pytest tests/test_phocr_output.py -v
```

### Run Specific Tests

```bash
# Run only extraction tests
pytest tests/test_phocr_output.py::TestExtractionAPI -v

# Run only verification tests
pytest tests/test_phocr_output.py::TestVerificationAPI -v

# Run only edge case tests
pytest tests/test_phocr_output.py::TestAPIEdgeCases -v

# Run tests for a specific image (e.g., image 1)
pytest tests/test_phocr_output.py -k "1.png" -v

# Run with detailed output
pytest tests/test_phocr_output.py -vv --tb=short

# Run with detailed output and print statements
pytest tests/test_phocr_output.py -vv -s
```

## Test Cases

### 1. Extraction API Tests

#### `test_extraction_consistency` (Parametrized - 3 images)
- **Purpose:** Tests the `/extract` endpoint with each test image 5 times
- **Validation:** Passes if extracted fields match expected output more than 3 times out of 5
- **Images Tested:** 1.png, 2.png, 3.png
- **Expected Fields:** Extracted text, confidence scores, bounding boxes

#### `test_extraction_with_detection_overlay`
- **Purpose:** Tests extraction with confidence overlay enabled
- **Validation:** Verifies that overlay image is returned as base64
- **Image:** 1.png

### 2. Verification API Tests

#### `test_verification_consistency` (Parametrized - 3 images)
- **Purpose:** Tests the `/verify` endpoint with each test image 5 times
- **Validation:** Passes if verification completes successfully more than 3 times out of 5
- **Images Tested:** 1.png, 2.png, 3.png
- **Verification Data:** Uses expected field values from extraction

#### `test_verification_field_results`
- **Purpose:** Validates detailed field-level verification results
- **Validation:** Checks similarity scores, status, and confidence for each field
- **Image:** 1.png

### 3. Edge Case Tests

#### `test_extraction_missing_file`
- **Purpose:** Tests API error handling with missing file
- **Expected:** API should return error status

#### `test_extraction_invalid_json_fields`
- **Purpose:** Tests API error handling with malformed JSON
- **Expected:** API should reject invalid input

#### `test_verification_empty_verification_data`
- **Purpose:** Tests API with empty verification data
- **Expected:** API should handle gracefully

## Expected Test Results

### Passing Criteria
- **Extraction Tests:** > 3 out of 5 iterations must match expected output
- **Verification Tests:** > 3 out of 5 iterations must complete successfully
- **Edge Case Tests:** API must return appropriate status codes

### Output Example
```
tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] PASSED
1.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[2.png] PASSED
2.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[3.png] PASSED
3.png - Extraction API: 4/5 iterations matched expected output

tests/test_phocr_output.py::TestVerificationAPI::test_verification_consistency[1.png] PASSED
1.png - Verification API: 5/5 iterations succeeded

tests/test_phocr_output.py::TestVerificationAPI::test_verification_consistency[2.png] PASSED
2.png - Verification API: 5/5 iterations succeeded

tests/test_phocr_output.py::TestVerificationAPI::test_verification_consistency[3.png] PASSED
3.png - Verification API: 5/5 iterations succeeded
```

## Test Configuration

### Customizing Expected Outputs

Edit `EXPECTED_OUTPUTS` dictionary in `test_phocr_output.py` to match your document images:

```python
EXPECTED_OUTPUTS = {
    "1.png": {
        "fields": ["field1", "field2", "field3"],  # Fields to extract
        "expected_mapped_fields": {
            "field1": "expected_value1",
            "field2": "expected_value2",
            "field3": "expected_value3",
        },
        "verification_data": {
            "field1": "expected_value1",
            "field2": "expected_value2",
            "field3": "expected_value3",
        },
    },
    # ... more images
}
```

### Adjusting Similarity Threshold

The `is_similar()` function uses a similarity threshold of 0.75 (75%). Adjust it for more/less strict matching:

```python
def is_similar(str1, str2, threshold=0.75):  # Change 0.75 to desired value
```

## Debugging Failed Tests

### 1. Verbose Output
```bash
pytest tests/test_phocr_output.py -vv -s
```

### 2. Show All Output
```bash
pytest tests/test_phocr_output.py -vv -s --capture=no
```

### 3. Run Single Test with Debugging
```bash
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] -vv -s --pdb
```

### 4. Check API Response
Add print statements or use the `--tb=short` flag:
```bash
pytest tests/test_phocr_output.py -vv --tb=short
```

## Common Issues

### Issue: "API server is not running"
**Solution:** Start the API server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Issue: "Test image not found"
**Solution:** Ensure images are in `backend/tests/Results/`:
```bash
ls backend/tests/Results/  # Check files exist
```

### Issue: "ModuleNotFoundError" for pytest or requests
**Solution:** Install test dependencies:
```bash
pip install pytest pytest-timeout requests
```

### Issue: Tests pass sometimes, fail other times
**This is expected!** ML model outputs vary. The 5-iteration approach with >3 match threshold accounts for this variance.

## Performance Notes

- Each test makes 5 API calls (ML operations can be slow)
- Total test suite runtime: ~5-15 minutes depending on system
- Use `--timeout=60` to set timeout for slow operations:
```bash
pytest tests/test_phocr_output.py --timeout=60
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: OCR API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-timeout
      - name: Start API server
        run: |
          cd backend
          uvicorn app.main:app --host 127.0.0.1 --port 8000 &
          sleep 5
      - name: Run tests
        run: |
          cd backend
          pytest tests/test_phocr_output.py -v
```

## Contributing

To add more test cases:

1. Add test images to `backend/tests/Results/`
2. Update `EXPECTED_OUTPUTS` with new image data
3. Add test methods to test classes
4. Run tests to verify

## License

Same as main project.
