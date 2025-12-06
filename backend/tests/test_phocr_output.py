import pytest
import requests
import json
import os
from pathlib import Path

# Base API URL
BASE_URL = "http://127.0.0.1:8000"
IMAGES_DIR = Path(__file__).parent / "Results"

# Define expected outputs for each image
# Note: These are approximate expected values - ML outputs can vary
EXPECTED_OUTPUTS = {
    "1.png": {
        "fields": ["Name", "Age", "Gender", "DOB", "Address", "Country", "Phone", "Email", "ID"],
        "mapped_fields": {
            "Name": "PRIYANKA KUMARI",
            "Age": "26 years old",
            "Gender": "Female",
            "DOB": "1995-06-17",
            "Address": "3WEKY5JOR4",
            "Country": "India",
            "Phone": "",
            "Email": "",
            "ID": "311c1cb7"
        },
    },
    "2.png": {
        "fields": ["Name", "Age", "Gender", "DOB", "Address", "Country", "Phone", "Email", "ID"],
        "mapped_fields": {
            "Name": "山田 井月",
            "Age": "",
            "Gender": "",
            "DOB": "1999年12月31日",
            "Address": "東京都世田谷区1丁目23番地45-6789号",
            "Country": "日本国 JAPAN",
            "Phone": "",
            "Email": "",
            "ID": ""
        }
    },
    "3.png": {
        "fields": ["Name", "Age", "Gender", "DOB", "Address", "Country", "Phone", "Email", "ID"],
        "mapped_fields": {
            "Name": "奥巴马",
            "Age": "",
            "Gender": "男",
            "DOB": "1961年8月4日",
            "Address": "华盛顿特区宜宾法尼亚大道1600号白宫 123456196108047890",
            "Country": "",
            "Phone": "",
            "Email": "",
            "ID": ""
        }
    }
}


class TestExtractionAPI:
    """Test cases for the OCR Extraction API"""

    @pytest.mark.parametrize("image_name", ["1.png", "2.png", "3.png"])
    def test_extraction_consistency(self, image_name):
        """
        Test extraction API 5 times for each image.
        Pass if output matches expected values more than 3 times out of 5.
        """
        image_path = IMAGES_DIR / image_name
        assert image_path.exists(), f"Test image {image_name} not found at {image_path}"

        expected = EXPECTED_OUTPUTS[image_name]
        fields = expected["fields"]
        expected_mapped_fields = expected["mapped_fields"]

        matches = 0
        extraction_results = []
        errors = []

        for iteration in range(5):
            print(f"\n{image_name} - Iteration {iteration + 1}/5 starting...")
            try:
                # Prepare request
                with open(image_path, "rb") as f:
                    files = {"document": (image_name, f, "image/png")}
                    data = {
                        "include_detection": "false",
                        "fields": json.dumps(fields),
                    }

                    # Send extraction request
                    response = requests.post(
                        f"{BASE_URL}/extract",
                        files=files,
                        data=data,
                        timeout=180,
                    )

                if response.status_code != 200:
                    error_msg = f"Iteration {iteration + 1}: Status {response.status_code}"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue

                result = response.json()
                extraction_results.append(result)

                # Verify response structure
                if "mapped_fields" not in result:
                    error_msg = f"Iteration {iteration + 1}: Response missing 'mapped_fields'"
                    print(f"❌ {error_msg}")
                    errors.append(error_msg)
                    continue

                # Check if extraction matches expected output (case-insensitive)
                if result.get("mapped_fields"):
                    matches_this_iteration = True
                    for field, expected_value in expected_mapped_fields.items():
                        if expected_value and expected_value.strip():  # Only check non-empty expected values
                            extracted_value = result.get("mapped_fields", {}).get(field, "")
                            if extracted_value:
                                extracted_lower = str(extracted_value).lower().strip()
                                expected_lower = str(expected_value).lower().strip()
                                # Use fuzzy matching to account for minor OCR variations
                                if not is_similar(extracted_lower, expected_lower):
                                    matches_this_iteration = False
                                    break

                    if matches_this_iteration:
                        matches += 1
                        print(f"✓ Iteration {iteration + 1}: MATCH ({matches}/5)")
                    else:
                        print(f"✗ Iteration {iteration + 1}: No match")
                    
                    print(f"  Extracted: {result.get('mapped_fields')}")

            except requests.exceptions.Timeout as e:
                error_msg = f"Iteration {iteration + 1}: Request timeout after 180s"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
            except requests.exceptions.RequestException as e:
                error_msg = f"Iteration {iteration + 1}: Request failed - {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
            except Exception as e:
                error_msg = f"Iteration {iteration + 1}: Unexpected error - {str(e)}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)

        # Test passes if more than 3 out of 5 iterations match
        print(f"\n{'='*60}")
        print(f"{image_name} - FINAL RESULT: {matches}/5 iterations matched")
        print(f"Errors encountered: {len(errors)}")
        if errors:
            for error in errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        
        assert matches > 3, (
            f"Extraction test failed for {image_name}: Only {matches}/5 iterations "
            f"matched expected output (need > 3).\n"
            f"Errors: {errors}\n"
            f"Results: {extraction_results}"
        )

    def test_extraction_with_detection_overlay(self):
        """Test extraction API with detection overlay enabled"""
        image_name = "1.png"
        image_path = IMAGES_DIR / image_name
        assert image_path.exists(), f"Test image {image_name} not found"

        expected = EXPECTED_OUTPUTS[image_name]
        fields = expected["fields"]

        with open(image_path, "rb") as f:
            files = {"document": (image_name, f, "image/png")}
            data = {
                "include_detection": "true",
                "fields": json.dumps(fields),
            }

            response = requests.post(
                f"{BASE_URL}/extract",
                files=files,
                data=data,
                timeout=180,
            )

        assert response.status_code == 200
        result = response.json()

        # Verify confidence overlay is present
        assert "confidence_overlay" in result, "Response missing 'confidence_overlay'"
        assert result.get("has_detection_data") is True, "has_detection_data should be True"
        assert result.get("confidence_overlay"), "confidence_overlay should not be empty"

        print("✓ Extraction with detection overlay test passed")


class TestAPIEdgeCases:
    """Test edge cases and error handling"""

    def test_extraction_missing_file(self):
        """Test extraction API with missing file"""
        data = {
            "include_detection": "false",
            "fields": json.dumps(["name"]),
        }

        response = requests.post(
            f"{BASE_URL}/extract",
            files={"document": None},
            data=data,
            timeout=180,
        )

        # Should return error
        assert response.status_code != 200, "API should reject missing file"

    def test_extraction_invalid_json_fields(self):
        """Test extraction API with invalid JSON fields"""
        image_path = IMAGES_DIR / "1.png"
        if not image_path.exists():
            pytest.skip("Test image not found")

        with open(image_path, "rb") as f:
            files = {"document": ("1.png", f, "image/png")}
            data = {
                "include_detection": "false",
                "fields": "not valid json",  # Invalid JSON
            }

            response = requests.post(
                f"{BASE_URL}/extract",
                files=files,
                data=data,
                timeout=180,
            )

        # Should return error or handle gracefully
        assert response.status_code != 200, "API should reject invalid JSON fields"


# ============================================================================
# Utility Functions
# ============================================================================


def is_similar(str1, str2, threshold=0.75):
    """
    Check if two strings are similar using a simple similarity metric.
    This accounts for minor OCR variations and typos.

    Args:
        str1: First string
        str2: Second string
        threshold: Similarity threshold (0-1)

    Returns:
        bool: True if strings are similar enough
    """
    if not str1 or not str2:
        return str1 == str2

    # Check exact match
    if str1 == str2:
        return True

    # Check if one is contained in the other (for partial matches)
    if str1 in str2 or str2 in str1:
        return True

    # Simple Levenshtein-like similarity
    # Count matching characters
    matches = sum(1 for a, b in zip(str1, str2) if a == b)
    max_len = max(len(str1), len(str2))

    if max_len == 0:
        return True

    similarity = matches / max_len
    return similarity >= threshold


@pytest.fixture(scope="session")
def api_server_running():
    """
    Fixture to check if the API server is running.
    Fails the entire test session if server is not available.
    """
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        assert response.status_code in [200, 404], "API server not responding correctly"
        print("✓ API server is running and accessible")
    except requests.exceptions.ConnectionError:
        pytest.fail(
            f"API server is not running at {BASE_URL}. "
            f"Please start the server with: uvicorn app.main:app --reload"
        )
    except Exception as e:
        pytest.fail(f"Error checking API server: {str(e)}")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers",
        "extraction: mark test as extraction API test",
    )
    config.addinivalue_line(
        "markers",
        "edge_cases: mark test as edge case test",
    )
