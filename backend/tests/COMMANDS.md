# OCR API Test Suite - Complete Command Reference

## 🚀 One-Time Setup

### Windows
```powershell
cd backend\tests
setup.bat
```

### Linux/Mac
```bash
cd backend/tests
bash setup.sh
```

### Manual Setup (All Platforms)
```bash
cd backend
pip install pytest pytest-timeout requests
```

---

## 🎯 Running Tests

### Start API Server (Terminal 1)
```bash
cd backend
.venv\Scripts\activate              # Windows
# source .venv/bin/activate         # Linux/Mac
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Run Tests (Terminal 2)
```bash
cd backend
.venv\Scripts\activate              # Windows
# source .venv/bin/activate         # Linux/Mac
pytest tests/test_phocr_output.py -v
```

---

## 📊 Different Test Commands

### Run All Tests
```bash
pytest tests/test_phocr_output.py -v
```

### Run Tests with Output
```bash
pytest tests/test_phocr_output.py -v -s
```

### Run Tests with Verbose Output
```bash
pytest tests/test_phocr_output.py -vv -s
```

### Run Only Extraction Tests
```bash
pytest tests/test_phocr_output.py::TestExtractionAPI -v
```

### Run Only Verification Tests
```bash
pytest tests/test_phocr_output.py::TestVerificationAPI -v
```

### Run Only Edge Case Tests
```bash
pytest tests/test_phocr_output.py::TestAPIEdgeCases -v
```

### Run Tests for Specific Image
```bash
pytest tests/test_phocr_output.py -k "1.png" -v
pytest tests/test_phocr_output.py -k "2.png" -v
pytest tests/test_phocr_output.py -k "3.png" -v
```

### Run Single Test
```bash
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] -v
```

### Run with Timeout
```bash
pytest tests/test_phocr_output.py -v --timeout=60
```

### Run with Detailed Errors
```bash
pytest tests/test_phocr_output.py -vv --tb=long
```

### Run with Short Errors
```bash
pytest tests/test_phocr_output.py -v --tb=short
```

### Run Until First Failure
```bash
pytest tests/test_phocr_output.py -v -x
```

### Run Last Failed Tests
```bash
pytest tests/test_phocr_output.py -v --lf
```

### Run Tests and Generate Report
```bash
pytest tests/test_phocr_output.py -v --html=report.html
```

---

## 🔄 Development Workflow

### 1. Start Development
```bash
cd backend
.venv\Scripts\activate
```

### 2. Update Expected Values
Edit `test_phocr_output.py` and update `EXPECTED_OUTPUTS` dictionary

### 3. Run Tests
```bash
pytest tests/test_phocr_output.py -v -s
```

### 4. View Output
```
test_extraction_consistency[1.png] PASSED
1.png - Extraction API: 4/5 iterations matched expected output
```

### 5. Iterate Until Tests Pass
- Repeat steps 2-4 until tests pass
- Aim for >3/5 match rate (60%)

---

## 🛠️ Debugging

### Run Single Test with Debug
```bash
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] -vv -s --tb=long
```

### Run with Python Debugger
```bash
pytest tests/test_phocr_output.py -v -s --pdb
```

### Run with Print Statements
```bash
pytest tests/test_phocr_output.py -v -s --capture=no
```

### Show Full Error Traceback
```bash
pytest tests/test_phocr_output.py -v --tb=long
```

---

## 📝 Log and Output Management

### Save Results to File
```bash
pytest tests/test_phocr_output.py -v > test_results.txt
```

### Save Results with Timestamp
```bash
pytest tests/test_phocr_output.py -v > results_$(date +%Y%m%d_%H%M%S).txt
```

### Generate HTML Report
```bash
pytest tests/test_phocr_output.py -v --html=report.html --self-contained-html
```

### Generate JUnit XML
```bash
pytest tests/test_phocr_output.py -v --junit-xml=report.xml
```

---

## 🚨 Troubleshooting Commands

### Check Python Installation
```bash
python --version
python -m pip --version
```

### Check Virtual Environment
```bash
where python              # Windows
which python             # Linux/Mac
```

### Install Missing Dependencies
```bash
pip install pytest pytest-timeout requests
```

### Upgrade pytest
```bash
pip install --upgrade pytest
```

### Check API Status
```bash
curl http://127.0.0.1:8000/docs
```

### List Test Files
```bash
pytest tests/ --collect-only
```

### List Test Functions
```bash
pytest tests/test_phocr_output.py --collect-only
```

---

## 📊 Report Generation

### Using Test Report Generator
```python
from tests.test_report_generator import TestReport

report = TestReport()
report.add_test_result("test_name", "passed")
report.generate_html_report("my_report.html")
report.generate_json_report("my_report.json")
report.print_summary()
```

### Example Script
```bash
# Create run_tests.py
python -m pytest tests/test_phocr_output.py -v
```

---

## ⚙️ Configuration Commands

### Check Pytest Configuration
```bash
pytest --co -q tests/test_phocr_output.py
```

### Show Pytest Fixtures
```bash
pytest --fixtures tests/test_phocr_output.py
```

### Lint Check (Optional)
```bash
pip install pylint
pylint tests/test_phocr_output.py
```

### Format Code (Optional)
```bash
pip install black
black tests/test_phocr_output.py
```

---

## 🔐 Production/CI Commands

### Run Tests in Headless Mode
```bash
pytest tests/test_phocr_output.py -v --tb=short -q
```

### Run with Coverage
```bash
pip install pytest-cov
pytest tests/test_phocr_output.py --cov=app --cov-report=html
```

### Run Parallel Tests (Faster)
```bash
pip install pytest-xdist
pytest tests/test_phocr_output.py -v -n auto
```

### Run with Timeout (Prevent Hanging)
```bash
pytest tests/test_phocr_output.py -v --timeout=300
```

---

## 📦 Dependency Commands

### List Installed Packages
```bash
pip list
```

### List Test Dependencies
```bash
pip list | findstr pytest
pip list | grep pytest    # Linux/Mac
```

### Export Current Environment
```bash
pip freeze > test_requirements.txt
```

### Install from Requirements
```bash
pip install -r test_requirements.txt
```

---

## 🔄 Continuous Testing (Watch Mode)

### Auto-run Tests on File Change (Optional)
```bash
pip install pytest-watch
ptw tests/
```

### Run Tests Every 5 Minutes
```bash
watch -n 300 "pytest tests/test_phocr_output.py -v"
```

---

## 🗑️ Cleanup Commands

### Remove Test Cache
```bash
rm -rf tests/__pycache__
rm -rf tests/.pytest_cache
del /s tests\__pycache__    # Windows
```

### Remove Generated Reports
```bash
rm test_results.txt report.html report.xml
del test_results.txt report.html report.xml  # Windows
```

### Clean All Generated Files
```bash
pytest tests/ --collect-only -q
```

---

## 📋 Quick Reference Table

| Command | Purpose | Time |
|---------|---------|------|
| `pytest tests/test_phocr_output.py -v` | Run all tests | 5-15 min |
| `pytest tests/test_phocr_output.py::TestExtractionAPI -v` | Extraction only | 2-5 min |
| `pytest tests/test_phocr_output.py -k "1.png" -v` | Image 1 tests | 1-3 min |
| `pytest tests/test_phocr_output.py -v -s` | With output | 5-15 min |
| `pytest tests/test_phocr_output.py -vv -s` | Verbose | 5-15 min |
| `pytest tests/test_phocr_output.py --collect-only` | List tests | <1 sec |

---

## 🎓 Learning Commands

### See All Available Options
```bash
pytest --help
pytest --help | less
```

### Show Markers
```bash
pytest --markers
```

### Show Config
```bash
pytest --co
pytest --co -q
```

### Run in Quiet Mode
```bash
pytest -q tests/test_phocr_output.py
```

### Run in Verbose Mode
```bash
pytest -vv tests/test_phocr_output.py
```

---

## 🚀 Production Deployment Commands

### For GitHub Actions
```yaml
- name: Run OCR Tests
  run: |
    cd backend
    pip install pytest pytest-timeout requests
    uvicorn app.main:app &
    sleep 5
    pytest tests/test_phocr_output.py -v
```

### For Docker
```bash
docker run --rm -v $(pwd):/workspace python:3.9 \
  sh -c "cd /workspace/backend && pip install -r requirements.txt && pytest tests/test_phocr_output.py -v"
```

### For Jenkins
```groovy
stage('Test') {
  steps {
    sh 'cd backend && pip install pytest requests'
    sh 'cd backend && pytest tests/test_phocr_output.py -v'
  }
}
```

---

## 💡 Pro Tips

### Run Specific Test with Debugging
```bash
pytest tests/test_phocr_output.py::TestExtractionAPI::test_extraction_consistency[1.png] -vv -s --pdb
```

### Save Detailed Report
```bash
pytest tests/test_phocr_output.py -v --tb=long > detailed_report.txt
```

### Run Tests in Parallel (Faster)
```bash
pip install pytest-xdist
pytest tests/test_phocr_output.py -n auto
```

### Monitor Test Execution
```bash
pytest tests/test_phocr_output.py -v -s --durations=10
```

### Skip Specific Test
```bash
pytest tests/test_phocr_output.py -v -k "not edge_cases"
```

---

**Last Updated:** December 2025
**Python Version:** 3.8+
**Pytest Version:** 7.0+

For more help, see: backend/tests/README.md
