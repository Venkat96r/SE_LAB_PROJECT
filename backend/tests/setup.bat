@echo off
REM Setup script for OCR API Test Suite (Windows)
REM Run this script to automatically install and configure the test suite

cls
echo ==========================================
echo OCR API Test Suite - Setup Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "backend\.venv" (
    echo 📦 Creating virtual environment...
    cd backend
    python -m venv .venv
    cd ..
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Install dependencies
echo 📥 Installing test dependencies...
call backend\.venv\Scripts\activate.bat
pip install pytest pytest-timeout requests >nul 2>&1
echo ✅ Dependencies installed
echo.

REM Check if test images exist
echo 🖼️  Checking test images...
if exist "backend\tests\Results\1.png" (
    if exist "backend\tests\Results\2.png" (
        if exist "backend\tests\Results\3.png" (
            echo ✅ All test images found
            goto imagecheck_done
        )
    )
)
echo ⚠️  Warning: Some test images may be missing
echo    Expected: backend\tests\Results\1.png, 2.png, 3.png
:imagecheck_done
echo.

REM Display next steps
echo ==========================================
echo Setup Complete! ✅
echo ==========================================
echo.
echo Next steps:
echo.
echo 1. Start the API server (in Terminal 1):
echo    cd backend
echo    .venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 2. Run tests (in Terminal 2):
echo    cd backend
echo    .venv\Scripts\activate
echo    pytest tests/test_phocr_output.py -v
echo.
echo 📖 Documentation:
echo    - Quick start: backend\tests\QUICK_START.md
echo    - Full guide: backend\tests\README.md
echo    - Reference: backend\tests\REFERENCE_CARD.md
echo.
echo ==========================================
echo.
pause
