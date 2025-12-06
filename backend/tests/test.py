import pytest
import requests
import json
import os
from pathlib import Path

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/extract"
VERIFY_URL = "http://127.0.0.1:8000/verify"  # Assuming a separate /verify endpoint
# Assuming 'Images' folder is sibling to this test file.
IMAGES_DIR = Path(__file__).parent / "Images"

# Define expected outputs for all test images
EXPECTED_OUTPUTS = {
    "1.png":{
        "fields": ["Name", "Age", "Gender", "DOB", "Address", "Country"],
        "mapped_fields": {
            "Name": "樂永晴",
            "Age": "31岁",
            "Gender": "女",
            "DOB": "1985年6月3日",
            "Address": "香港",
            "Country": "中国香港"
        },  
    },
    # ADDING 2.png placeholder for the error test case
    "2.png": {
        "fields": ["Name", "Age", "Gender", "DOB", "Address"],
        "mapped_fields": {}, # Empty mapped fields, as extraction will fail
    },
    "3.png": {
        "fields": ["Name", "Age", "Gender", "DOB", "Phone", "Email"],
        "mapped_fields": {
            "Name": "Vaishnavi Singh",
            "Age": "23",
            "Gender": "FEMALE",
            "DOB": "16/11/2004",
            "Phone": "8911 3824 2345",
            "Email": "DOB: 16/11/2004",
        }
    },
    "6.jpeg": {
        "fields": ["Name", "Gender", "DOB", "Address"],
        "mapped_fields": {
            "Name": "奥巴马",
            "Gender": "男",
            "DOB": "1961年8月4日",
            "Address": "华盛顿特区宜宾法尼亚大道1600号白宫 123456196108047890"
        }
    },
    "4.jpg": {
        "fields": ["Name", "Age", "Gender", "DOB", "Country"],
        "mapped_fields": {
            "Name": "PRIYANKA KUMARI",
            "Age": "26 years old",
            "Gender": "Female",
            "DOB": "1995-06-17",
            "Country": "India"
        },
    },
    "5.jpg": {
        "fields": ["Name", "DOB", "Address", "Country"],
        "mapped_fields": {
            "Name": "山田 井月",
            "DOB": "1999年12月31日",
            "Address": "東京都世田谷区1丁目23番地45-6789号",
            "Country": "日本国 JAPAN"
        }
    },
    "7.png": {
        "fields": ["Name", "Age", "Gender", "Address", "Country", "Phone", "Email"],
        "mapped_fields": {
            "Name": "John Smith",
            "Age": "30",
            "Gender": "Male",
            "Address": "I23 ElmSt",
            "Country": "USA",
            "Phone": "555-12345",
            "Email": "john.smith@example.com",
        }
    },
    "8.png": {
        "fields": ["Name", "Age", "Gender", "Address", "Country", "Phone", "Email"],
        "mapped_fields": {
            "Name": "Ananya Sharma",
            "Age": "29",
            "Gender": "Female",
            "Address": "123, MG Road, Bengaluru, Karnataka - 560001",
            "Country": "India",
            "Phone": "+91-9876543210",
            "Email": "ananya.sharma@example.com"
        }
    }
}

# --- Expected Error Response for Poor Quality Image ---
EXPECTED_POOR_QUALITY_RESPONSE = {
    "error": "Image quality too poor for reliable OCR.",
    "quality": {
        "score": 15,
        "suggestions": [
            "Image resolution is too low. Please upload a higher resolution image.",
            "The image is severely blurred and text is not readable. Please capture a much sharper photo.",
            "Low contrast detected. Use better lighting or ensure clear text visibility."
        ],
        "blur_details": {
            "overall_blur_score": 0.11151102767577539,
            "individual_scores": {
                "laplacian": 1.2415910176779743,
                "sobel": 85.5593884376493,
                "gradient_mean": 6.820050133994336,
                "gradient_std": 6.2487042342755466,
                "high_freq": 3.786797582621183,
                "text_blur": 0.0,
                "edge_sharpness": 0.0,
                "multiscale": 0.22989655008155946
            },
            "text_clarity": 0.5953293593903266
        }
    }
}


# --- Utility Functions for Fuzzy Matching ---

def is_similar(str1, str2, threshold=0.60):
    """
    Checks if two strings are similar enough for OCR validation (60% similarity threshold).
    """
    if not str1 or not str2:
        return str1 == str2

    str1 = str(str1).lower().strip()
    str2 = str(str2).lower().strip()

    if str1 == str2:
        return True
    
    # Simple Levenshtein-like similarity check
    matches = sum(1 for a, b in zip(str1, str2) if a == b)
    max_len = max(len(str1), len(str2))

    if max_len == 0:
        return True

    similarity = matches / max_len
    return similarity >= threshold

# --- Pytest Class and Test Function ---

class TestExtractionConsistency:

    # NOTE: Modified to skip 2.png for this test, as it's tested separately for rejection.
    @pytest.mark.parametrize("image_name", [name for name in EXPECTED_OUTPUTS.keys() if name != "2.png"])
    def test_extraction_threshold_match(self, image_name):
        # ... (Existing test_extraction_threshold_match logic remains the same for other images)
        image_path = IMAGES_DIR / image_name
        assert image_path.exists(), f"Test image {image_name} not found at {image_path}"

        expected_data = EXPECTED_OUTPUTS[image_name]
        fields = expected_data["fields"]
        expected_mapped_fields = expected_data["mapped_fields"]

        # 1. Determine the non-empty expected fields for the threshold calculation
        expected_non_empty_fields = {
            k: v for k, v in expected_mapped_fields.items() if v and v.strip()
        }
        total_fields_to_check = len(expected_non_empty_fields)
        
        # If no fields are expected to be extracted, the test passes immediately.
        if total_fields_to_check == 0:
            print(f"Skipping {image_name}: No non-empty fields expected for comparison.")
            return

        # Calculate required matches (60% of total non-empty fields)
        required_matches = total_fields_to_check * 0.60
        required_matches = max(1, int(required_matches) if required_matches == int(required_matches) else int(required_matches) + 1)
        
        print(f"\n{'='*60}")
        print(f"Image: {image_name} | Total Fields to Check: {total_fields_to_check}")
        print(f"Required Matches (60%): {required_matches}")
        print(f"{'='*60}")
        
        # 2. Prepare and Send Request
        try:
            # Determine correct MIME type (image/jpeg or image/png)
            mime_type = "image/jpeg" if image_path.suffix.lower() in [".jpeg", ".jpg"] else "image/png"
            
            with open(image_path, "rb") as f:
                files = {"document": (image_name, f, mime_type)}
                data = {
                    "include_detection": "false",
                    "fields": json.dumps(fields),
                    "language": "en" 
                }
                
                # Send extraction request
                response = requests.post(
                    f"{API_URL}",
                    files=files,
                    data=data,
                )

            # 3. Basic Validation
            assert response.status_code == 200, (
                f"API failed for {image_name}. Status code: {response.status_code}. "
                f"Response text: {response.text}"
            )

            result = response.json()
            assert "mapped_fields" in result, "Response missing 'mapped_fields' key."
            extracted_mapped_fields = result.get("mapped_fields", {})

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed for {image_name}: {str(e)}")
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON response for {image_name}: {response.text}")

        # 4. Fuzzy Matching and Threshold Check
        
        successful_matches = 0
        mismatch_details = {}

        for field, expected_value in expected_non_empty_fields.items():
            extracted_value = extracted_mapped_fields.get(field, "")
            
            if is_similar(extracted_value, expected_value, threshold=0.60):
                successful_matches += 1
            else:
                mismatch_details[field] = {
                    "Expected": expected_value, 
                    "Actual": extracted_value
                }

        print(f"\nFinal Score: {successful_matches}/{total_fields_to_check} fields matched.")

        # Final assertion against the 60% threshold
        assert successful_matches >= required_matches, (
            f"Extraction test FAILED for {image_name}. "
            f"Expected fields matched: {successful_matches}/{total_fields_to_check}. "
            f"Needed: {required_matches} matches (60%).\n"
            f"Mismatch Details: {json.dumps(mismatch_details, ensure_ascii=False, indent=2)}"
        )
    
    
    # --------------------------------------------------------------------------
    # NEW TEST CASE: POOR QUALITY IMAGE REJECTION
    # --------------------------------------------------------------------------

    def test_poor_quality_image_rejection(self):
        """
        Tests sending a known poor-quality image (2.png) and asserts that the 
        API correctly rejects it with a specific error structure and a non-200 status.
        """
        image_name = "2.png"
        image_path = IMAGES_DIR / image_name
        assert image_path.exists(), f"Test image {image_name} not found at {image_path}"
        
        # We need fields for the API call, even though we expect failure
        fields = EXPECTED_OUTPUTS[image_name]["fields"]
        
        print(f"\n{'='*60}")
        print(f"Testing Poor Quality Image Rejection: {image_name}")
        print(f"{'='*60}")

        try:
            mime_type = "image/png"
            with open(image_path, "rb") as f:
                files = {"document": (image_name, f, mime_type)}
                data = {
                    "include_detection": "false",
                    "fields": json.dumps(fields),
                    "language": "en" 
                }
                
                # Send extraction request
                response = requests.post(
                    f"{API_URL}",
                    files=files,
                    data=data,
                )

            # 1. Assert non-200 status code (e.g., 400 Bad Request)
            # The API should clearly indicate a client error for poor input quality.
            assert response.status_code == 400, (
                f"Expected status code 400 for poor quality image, but got {response.status_code}. "
                f"Response: {response.text}"
            )

            # 2. Assert the specific error structure
            result = response.json()
            
            # Check top-level keys
            assert "error" in result, "Error response missing 'error' key."
            assert "quality" in result, "Error response missing 'quality' key."
            
            # Check error message (fuzzy match on the main error message)
            assert is_similar(result["error"], EXPECTED_POOR_QUALITY_RESPONSE["error"]), (
                f"Error message mismatch. Expected similar to: '{EXPECTED_POOR_QUALITY_RESPONSE['error']}', "
                f"Actual: '{result['error']}'"
            )

            # Check suggestions list (must be a list and contain at least one suggestion)
            assert isinstance(result["quality"].get("suggestions"), list)
            assert len(result["quality"]["suggestions"]) > 0

            print("✓ Poor quality image successfully rejected with expected error structure (Status 400).")

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed for {image_name}: {str(e)}")
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON response from rejection endpoint for {image_name}: {response.text}")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred during rejection test for {image_name}: {str(e)}")


    # --------------------------------------------------------------------------
    # NEW TEST CASE: /verify endpoint (Parameterized for ALL images)
    # --------------------------------------------------------------------------

    @pytest.mark.parametrize("image_name", [name for name in EXPECTED_OUTPUTS.keys() if name != "2.png"])
    def test_verification_endpoint(self, image_name):
        # ... (Existing test_verification_endpoint logic remains the same)
        image_path = IMAGES_DIR / image_name
        assert image_path.exists(), f"Test image {image_name} not found at {image_path}"
        
        # 1. Define the Verification Data Payload
        # Use the expected mapped_fields for the current image as the verification_data
        VERIFICATION_DATA = EXPECTED_OUTPUTS[image_name]["mapped_fields"]
        
        # All fields being requested for verification
        REQUEST_FIELDS = EXPECTED_OUTPUTS[image_name]["fields"]
        
        # 2. Prepare the Request
        try:
            mime_type = "image/jpeg" if image_path.suffix.lower() in [".jpeg", ".jpg"] else "image/png"
            
            with open(image_path, "rb") as f:
                files = {"document": (image_name, f, mime_type)}
                
                # Form data fields must be JSON-stringified for multipart request
                data = {
                    "verification_data": json.dumps(VERIFICATION_DATA, ensure_ascii=False),
                    "fields": json.dumps(REQUEST_FIELDS),
                }

                print(f"\n{'='*60}")
                print(f"Testing Verification Endpoint: {VERIFY_URL} with {image_name}")
                print(f"{'='*60}")
                
                # 3. Send the POST request
                response = requests.post(
                    VERIFY_URL,
                    files=files,
                    data=data,
                    # Added required header
                    headers={'Referrer-Policy': 'strict-origin-when-cross-origin'} 
                )

            # 4. Basic Validation
            assert response.status_code == 200, (
                f"Verification API failed for {image_name}. Status code: {response.status_code}. "
                f"Response text: {response.text}"
            )
            
            result = response.json()
            assert "verification_result" in result, "Verification response missing 'verification_result' key."
            verification_result = result.get("verification_result", {})
            
            # 5. Confidence Check
            assert "overall_confidence" in verification_result, "'verification_result' missing 'overall_confidence'."
            
            overall_confidence = verification_result["overall_confidence"]
            EXPECTED_CONFIDENCE_THRESHOLD = 0.70 # 70%

            print(f"Overall Confidence for {image_name}: {overall_confidence * 100:.2f}%")
            
            # Final Assertion
            assert overall_confidence > EXPECTED_CONFIDENCE_THRESHOLD, (
                f"Verification test FAILED for {image_name}: Overall confidence ({overall_confidence * 100:.2f}%) "
                f"is not greater than the required {EXPECTED_CONFIDENCE_THRESHOLD * 100:.0f}% threshold."
            )
            print(f"✓ Verification test passed for {image_name}.")

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Verification Request failed for {image_name}: {str(e)}")
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON response from verification endpoint for {image_name}: {response.text}")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred during verification test for {image_name}: {str(e)}")