#!/bin/bash
# Setup script for OCR API Test Suite
# Run this script to automatically install and configure the test suite

echo "=========================================="
echo "OCR API Test Suite - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "backend/.venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python -m venv .venv
    cd ..
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -f "backend/.venv/Scripts/activate" ]; then
    # Windows
    source backend/.venv/Scripts/activate
elif [ -f "backend/.venv/bin/activate" ]; then
    # Unix/Linux
    source backend/.venv/bin/activate
fi
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing test dependencies..."
pip install pytest pytest-timeout requests >/dev/null 2>&1
echo "✅ Dependencies installed"
echo ""

# Check if test images exist
echo "🖼️  Checking test images..."
if [ -f "backend/tests/Results/1.png" ] && [ -f "backend/tests/Results/2.png" ] && [ -f "backend/tests/Results/3.png" ]; then
    echo "✅ All test images found"
else
    echo "⚠️  Warning: Some test images may be missing"
    echo "   Expected: backend/tests/Results/1.png, 2.png, 3.png"
fi
echo ""

# Display next steps
echo "=========================================="
echo "Setup Complete! ✅"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the API server (in Terminal 1):"
echo "   cd backend"
echo "   .venv\\Scripts\\activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Run tests (in Terminal 2):"
echo "   cd backend"
echo "   .venv\\Scripts\\activate"
echo "   pytest tests/test_phocr_output.py -v"
echo ""
echo "📖 Documentation:"
echo "   - Quick start: backend/tests/QUICK_START.md"
echo "   - Full guide: backend/tests/README.md"
echo "   - Reference: backend/tests/REFERENCE_CARD.md"
echo ""
echo "=========================================="
