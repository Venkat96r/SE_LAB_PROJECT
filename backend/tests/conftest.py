"""
Pytest configuration and fixtures for OCR API tests
"""
import pytest
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def check_api_server():
    """
    Automatically check if the API server is running before running tests.
    This fixture is automatically used for all tests.
    """
    import time
    max_retries = 5
    retry_delay = 2

    print("\n" + "=" * 70)
    print("Checking if API server is running...")
    print("=" * 70)

    for attempt in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=5)
            if response.status_code in [200, 401]:
                print(f"✓ API server is running at {BASE_URL}")
                print("=" * 70)
                return
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                print(
                    f"  Attempt {attempt + 1}/{max_retries}: "
                    f"Server not responding, retrying in {retry_delay}s..."
                )
                time.sleep(retry_delay)
        except Exception as e:
            print(f"  Error: {str(e)}")

    pytest.fail(
        f"\n✗ API server is not running at {BASE_URL}\n"
        f"Please start the server with:\n"
        f"  cd backend\n"
        f"  .venv\\Scripts\\activate\n"
        f"  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
    )


@pytest.fixture
def images_dir():
    """Fixture providing path to test images directory"""
    return Path(__file__).parent / "Results"


@pytest.fixture
def test_image_1(images_dir):
    """Fixture providing path to first test image"""
    image_path = images_dir / "1.png"
    if not image_path.exists():
        pytest.skip(f"Test image not found: {image_path}")
    return image_path


@pytest.fixture
def test_image_2(images_dir):
    """Fixture providing path to second test image"""
    image_path = images_dir / "2.png"
    if not image_path.exists():
        pytest.skip(f"Test image not found: {image_path}")
    return image_path


@pytest.fixture
def test_image_3(images_dir):
    """Fixture providing path to third test image"""
    image_path = images_dir / "3.png"
    if not image_path.exists():
        pytest.skip(f"Test image not found: {image_path}")
    return image_path
