# Optical Character Recognition (OCR) for Text Extraction and Verification

A robust solution that uses Optical Character Recognition (OCR) to seamlessly extract text from scanned documents, intelligently auto-fill digital forms, and verify the extracted data.
Unlike most solutions that depend on cloud services or large models, our system can run fully offline, even on low-end computers. This makes it especially useful for adoption in remote areas without reliable network connectivity, ensuring accessibility and ease of setup anywhere.


## Walkthrough Video of Our Solution
[Youtube Link](https://youtu.be/kdGyAwhMve0)

## Project Report Link
[PDF Link](https://drive.google.com/file/d/1xuru5X1wfXgDTmBefvydxK9IY9Xc0ppL/view?usp=sharing)

##  Table of Contents

- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architectural Design](#architectural-design)
- [Challenges and Solutions](#challenges-and-solutions)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Test Case Explanation](#test-case-explanation)
  - [Extraction Test Cases (/extract Endpoint)](#extraction-test-cases-extract-endpoint)
  - [Quality and Verification( \verify endpoint) Test Cases](#quality-and-verification-verify-endpoint-test-cases)
- [API Documentation](#api-documentation)
  - [1. OCR Extraction API](#1-ocr-extraction-api)
  - [2. Data Verification API](#2-data-verification-api)

## Problem Statement
The process of manually extracting and verifiying information from physical documents like - application forms , ID cards , and certificates is inefficient and error prone.

The traditional process in not only slow but also introduces high risk of data entry mistakes and inconsistencies. These inaccuracies can lead to compromised data integrity and siginificant delays in critical processes. Our solution aims to replace this manual effort with automation that is fast , reliable and easy-to-use.

## Key Features
 1. **Automated Data Extraction**: 
 - Simply upload your document as a PDF or image to receive accurately extracted text in seconds, all while minimizing the errors commonly found in manual data entry.
 -  **Auto-Fill Digital Form** smartly using the extracted data for more accuratly and easily
 - **Multi-Lingual Support**  - Our project is equipped to handle complex international character sets. It offers robust supoort for not only Latin-Based languages but also suports Non-Latin languages such as Chinese, Japanese, and Korean.
 	 - **Automatic Language Detection**: The OCR pipeline automatically identifies the language in the document and applies the correct model, removing the need for manual selection.
   
 2. **Data Verification**: 
 - This feature acts as a crucial safety net to ensure the absolute accuracy of your data.

- It cross verifies the data entered in the digital form with the data from the  original scanned document field by field . Any mismatches will be flagged , and each field will be assigned a **confidence score** providing reliable measure for data accuracy.
3. **Image Quality analysis**: 
- **Automatic Scan Analysis**: The system first checks every document for common quality issues.
- **Detects Key Problems**: Every uploaded image is scored 0–100 before OCR to ensure accurate text extraction.
  The pipeline combines several computer-vision tests implemented with OpenCV, NumPy, and SciPy:

    - **Resolution** : Flags image smaller than 500px
    -  **Blur** : combines several detectors (edges, gradients, frequency content, text-region sharpness) into one overall blur score.
    - **Contrast** : measures global and local contrast to spot poor lighting.
    - **Text Clarity** : verifies clear character boundaries and line separation.
    - **Skew** : detects the page tilt and flags the error.
  Starting from 100, points are deducted for each issue and clear suggestions are returned.



4. **Multi-Page Document support**:
- **Handles Long Documents**: The system is built to process files containing multiple pages without issue.
- **Ensures Data Integrity**: It captures information from all pages and maintains the correct sequence, which is crucial for long forms.
5. **Real-time Confidence zones**: 
- **Instant Visual Feedback**: Provides immediate feedback by drawing bounding boxes directly on the original document image.
- **Shows OCR Confidence**: Each box is color-coded or labeled to show the confidence level of the text recognition inside it.
6. **Live Camera Capture**:
- Capture documents directly using the device camera for instant scanning and processing.
- Reduces the need for separate scanning hardware.
- Works in real time, enabling field agents or end-users to directly digitize paper forms on the spot.
  
  
7 . **Fully-Offline & Remote Friendly**:
- **Works without internet connectivity**, ensuring adoption in remote or low-connectivity regions.
- Protects data privacy by keeping all processing on local machines.
- Optimized to run even on low-end hardware , reducing infrastructure costs.
8. **User-Friendly Web Interface**:
- Modern, responsive design that works seamlessly across devices (desktop, tablet, mobile).
- Supports both dark mode and light mode for better user experience.
- Intuitive workflows ensure ease of use, even for non-technical users.
9. **Simple and Portable Setup**:
- The entire and system can be deployed with simple commands using Docker
- No cloud dependency , No External Configuration.
- Suitable for on-premise deployment in schools, offices, and government agencies in rural areas.

## Tech Stack
 - ### Backend :
    - OCR Model - PHOCR(PaddleOCR)
    - LLM for Intelligent Mapping - Qwen2.5-1.5B-Instruct
    - Server Logic - Python , FAST API
    - Ollama for offline functionality of LLM.
 - ### Frontend:
   - HTML /CSS
   - React.js


## Architectural Design
The system follows a modular, offline-first architecture designed for efficiency, scalability, and deployment in remote environments:
- **Input Layer** (Document/Image Capture): Accepts documents as PDFs, images, or live camera capture.
- **Pre-Processing Module**: Validates inputs by checking resolution, blur, contrast, and skew before OCR.
- **OCR & Data Extraction Engine**: Uses  PHOCR pipelines to extract multilingual text accurately.
- **LLM-based Intelligent Mapping**: Qwen2.5-1.5B is integrated via Ollama to map extracted data into structured digital forms.
- **Verification Module**: Performs field-level cross-checks between extracted data and original documents, assigning confidence scores.
- **Backend API (FastAPI)**: Manages communication between frontend, OCR, verification, and LLM services.
- **Deployment Layer** (Dockerized): Fully containerized for portability, offline setup, and easy deployment on low-resource machines.
  **Diagram**:
  <img width="2839" height="544" alt="diagram-export-10-5-2025-11_36_34-AM" src="https://github.com/user-attachments/assets/c3cd1048-dc88-4300-9902-1f5abd87e1d0" />


## Challenges and Solutions
 1. **Handling Tilted or Skewed Images**:
- **The Challenge**: The OCR model's accuracy dropped significantly when a document was tilted by more than 10° degrees, often failing to extract text correctly.

- **The Solution**: We integrated a deskewing algorithm into the image preprocessing pipeline. This automatically detects and corrects the rotational angle of any input document, ensuring the text is properly aligned before the OCR engine processes it. This step made our extraction far more reliable on real-world scans.
  
-  **The Result**: As a result, the system now maintains strong accuracy for images with skew angles of up to ±30°.
  


2. **Selecting the Optimal OCR Model**:
 -**The Challenge**: Our initial choice, TrOCR, performed well with Latin scripts but struggled with accuracy on our specific test data, especially with poor quality images.

-**The Solution**:We created a benchmark set of 50 images of varying quality (different resolutions, lighting conditions, and languages) and measured the accuracy of both TrOCR and PHOCR.
The results are shown in the graph below.
<img width="1641" height="983" alt="PhOCR vs TrOCR" src="https://github.com/user-attachments/assets/fba90ffa-7cab-4da0-a413-b2d510db2dcd" />



- **Test Results** : Both performed equally well for high quality images , but when it came to low quality and languages other than english PHOCR performed better than TrOCR.

 After comparative testing, we switched to the PHOCR model. It demonstrated superior overall accuracy and, crucially, performed exceptionally well with lower quality images as well, where TrOCR had failed.
 **FUNSD Dataset results** : PHOCR was evaluated on the FUNSD dataset.You can view the detailed test results [here]().It demonstrated excellent performance on this dataset.


3. **Ensuring Offline Functionality & Low-End Hardware Support**:
- **The Challange**: Many OCR + AI solutions rely on cloud APIs or require powerful GPUs, making them unusable in remote areas without reliable internet and on low-cost hardware. This risked excluding the very users who need automation most.
- **The Solution**: We re-architected the pipeline to run entirely offline, packaging OCR (PHOCR), LLM-based mapping (Qwen2.5-1.5B-Instruct), and FastAPI into a self-contained system. With lightweight optimization and Docker Compose setup, the solution can be launched in just two commands, even on machines with lower Hardware configurations.
- **The Result** : The system is now deployable in remote regions, supporting low-resource environments and enabling adoption by local governments and organizations. This aligns with MOSIP’s mission to provide inclusive, secure, and accessible digital identity solutions globally.
4. **Choosing a good Large-Language Model for Intelligent mapping**:
  - We experimented with several compact LLMs but found that most struggled to follow prompts accurately. Finally, we selected Qwen2.5-1.5B, which strikes the right balance between efficiency and performance. Despite its small size, it handles multilingual inputs exceptionally well and outperforms other lightweight models in accuracy and reliability.

  
## Getting Started 
### Backend Setup

**Prerequisites:**
- Python 3.10+
- pip
- Node.js (v18+) & npm
- Git
- Docker (optional, for containerized deployment)

**Installation:**
1. Clone the repository:
  ```bash
  git clone https://github.com/Venkat96r/SE_LAB_PROJECT.git
  ```
2. Move to the backend folder:
  ```bash
  cd backend
  ```
3. Create and activate a Python virtual environment:
  ```bash
  python -m venv .venv
  # On Windows:
  .venv\Scripts\activate
  # On Linux:
  source .venv/bin/activate
  ```
4. Install backend requirements:
  ```bash
  pip install -r requirements.txt
  ```
5. Ensure Docker is installed and running.
6. Pull the prebuilt image:
  ```bash
  docker pull venkat96r/ocr_backend:latest
  ```
7. Run the image:
  ```bash
  docker run -d -p 8000:8000 venkat96r/ocr_backend:latest
  ```
8. To run the tests, move to the tests folder within backend folder:
  ```bash
  cd tests
  ```
9. Run the tests:
  ```bash
  pytest test.py
  ```

### Frontend Setup
1. Move to the frontend folder:
  ```bash
  cd frontend
  ```
2. Install dependencies:
  ```bash
  npm install
  ```
3. Start the frontend:
  ```bash
  npm start
  ```


## Test Case Explanation:
The Pytest suite performs 15 tests across two main API endpoints (/extract and /verify) to ensure the reliability and functional completeness of the OCR pipeline, particularly in handling multilingual and poor-quality inputs.

### Extraction Test Cases (/extract Endpoint)
These 7 tests validate the core OCR engine and intelligent mapping.

**1. Extraction - Chinese (Traditional) - Module Test:**
Tests the ChineseExtractionModule by extracting Name, Age, Gender, DOB, Address, and Country from a document written in Traditional Chinese (1.png). This verifies the model's performance on complex international character sets.

**2. Extraction - Complex English Fields - Integration Test:**
Validates the system's ability to accurately extract structured, complex data types like Phone and Email from an English document (3.png), ensuring fields are parsed correctly despite varying formats. This test case tests the integration between extraction module and field mapping module.

**3. Extraction - Chinese (Simplified) - Module Test:**
Confirms Non-Latin Language Support by extracting key fields (Name, Gender, DOB, Address) from a document in Simplified Chinese (6.jpeg).

**4. Extraction - Standard English/Latin:**
Acts as a baseline accuracy test for the core extraction, processing standard Latin-based fields (Name, Age, Gender, DOB, Country) from an English document (4.jpg).

**5. Extraction - Japanese Language - Module Test:**
Tests the JapaneseExtractionModule by extracting Japanese characters, extracting Name, DOB, Address, and Country (5.jpg).

**6. Extraction - Full English Set:**
Verifies the extraction of a comprehensive set of standard English fields in a clean document (7.png), validating the complexity handled by the LLM mapping.

**7. Extraction - Complex Indian Address/Phone - Integration Test:** 
Tests the extraction of multi-line, structured, and challenging regional data formats.

### Quality and Verification( \verify endpoint) Test Cases
These 8 tests validate the Pre-Processing Module and the Data Verification API.

**8. Image Quality Analysis & Rejection: Module/Negative Testing:**
Sends a known poor-quality, blurred image (2.png) to the /extract endpoint. It asserts that the API returns the expected detailed JSON error structure and a non-200 status (validating the Image Quality Analysis feature). This ensures that our system handles the edge cases which involve poor quality images.

**9. Verification - Chinese (Traditional):**
Tests the Data Verification API by submitting the expected Traditional Chinese fields against the image (1.png)

**10. Verification - Complex English: Functional/Verification Test:**
Verifies the verification module's accuracy when checking complex English fields (Phone, Email) against the extracted data from (3.png).

**11. Verification - Chinese (Simplified): Functional/Verification Test:**
Tests the verification module's cross-check accuracy for Simplified Chinese fields (6.jpeg).

**12. Verification - Standard English: Functional/Verification Test:**
Confirms the verification module's high confidence score for standard English fields (4.jpg), ensuring the core verification logic works correctly.

**13. Verification - Japanese Language: Functional/Verification Test:**
Validates the verification module's handling of Japanese characters.

**14. Verification - Full English Set: Functional/Verification Test:**
Validates the verification endpoint's performance on a complete set of clean English data (7.png).

**15. Verification - Complex Indian Address/Phone: Functional/Verification Test:**
Verification - Complex Indian Address/Phone: Functional/Verification Test.

## API Documentation

The Postman collection is located at ```/backend/postman_collection```. Use it to test the backend API endpoints.
 1. **OCR Extraction API**

This API extracts text from a document image and maps the extracted text to given fields.

* **Endpoint**: `/extract` 
* **Method**: `POST` 
* **Headers**: `Content-Type: multipart/form-data`
* **Body** (form-data):
    * **document** (file): The image file of the document to be processed (e.g., `dummy_aadhaar.png`).
    * **include\_detection** (text): A boolean value ("true" or "false") to indicate whether to include detailed detection information in the response.
    * **fields** (text): A JSON array of strings representing the fields to be extracted from the document (e.g., `["name", "date of birth", "gender", "aadhaar number"]`).

### Successful Response (200 OK)

* **Content-Type**: `application/json` 
* **Body (JSON)**:
    * **mapped\_fields** (object): An object containing the extracted fields as key-value pairs.
        * **Example**: 
            ```json
            {
              "name": "Vaishnavi Singh",
              "date of birth": "16/11/2004",
              "gender": "FEMALE",
              "aadhaar number": "8911 3824 2345"
            }
            ```
           
    * **detections** (array): An array of objects, where each object represents a detected text block in the document. Each object contains:
        * `text` (string): The detected text.
        * `confidence` (number): The confidence score of the detection.
        * `bbox` (object): The bounding box of the detected text with coordinates `x1`, `y1`, `x2`, and `y2`.
        * `polygon` (array): The polygon coordinates of the detected text.
        * `confidence_level` (string): The confidence level of the detection (e.g., "low", "high").
    * **total\_detections** (number): The total number of text blocks detected.
    * **confidence\_overlay** (string): A base64 encoded image string of the document with confidence levels overlaid.
    * **has\_detection\_data** (boolean): A boolean indicating if detection data is available.
    * **processing\_info** (object): An object containing information about the processing of the document.
        * `language` (string): The language detected in the document.
        * `elapsed_time` (number): The time taken to process the document in seconds.
        * `page_number` (number): The page number of the document processed.
        * `is_pdf` (boolean): A boolean indicating if the document is a PDF.
        * `custom_fields_used` (number): The number of custom fields used for extraction.



 2. **Data Verification API**

This API verifies submitted data against the data extracted from a document image.

* **Endpoint**: `/verify` 
* **Method**: `POST` 
* **Headers**: `Content-Type: multipart/form-data`
* **Body** (form-data):
    * **document** (file): The image file of the document for verification.
    * **verification\_data** (text): A JSON object containing the key-value pairs to be verified against the document.
        * **Example**: 
            ```json
            {"Name": "John Smith", "age": "30", "gender": "Male", "address":"i23 elmst"}
            ```
          
    * **fields** (text): A JSON array of strings representing the fields to be verified.
        * **Example**: `["Name","age","gender","address"]` 

### Successful Response (200 OK)

* **success** (boolean): Indicates if the API call was successful.
* **verification\_result** (object): Contains the detailed results of the verification.
    * **overall\_status** (string): The overall verification status (e.g., "verified").
    * **overall\_confidence** (number): The overall confidence score of the verification (e.g., 100).
    * **field\_results** (object): An object detailing the verification for each submitted field, including the submitted value, extracted value, similarity score, status, and confidence.
    * **debug\_info** (object): Provides debugging information like the fields submitted and extracted.

 
   
