## Test Cases

Test cases for the backend are located in the `backend/tests/` directory. Currently, these are dummy tests provided as placeholders. You can expand or replace them with real tests as you develop and enhance the backend functionality.



# Optical Character Recognition (OCR) for Text Extraction and Verification

A robust solution that uses Optical Character Recognition (OCR) to seamlessly extract text from scanned documents, intelligently auto-fill digital forms, and verify the extracted data.
Unlike most solutions that depend on cloud services or large models, our system can run fully offline, even on low-end computers. This makes it especially useful for adoption in remote areas without reliable network connectivity, ensuring accessibility and ease of setup anywhere.


## Walkthrough Video of Our Solution
[Youtube Link](https://youtu.be/kdGyAwhMve0)

## Folder Structure

```
SE_LAB_PROJECT/
│   Dockerfile
│   entrypoint.sh
│   README.md
│
├── backend/
│   ├── requirements.txt
│   ├── uploads/
│   ├── postman_collection/
│   │   └── OCR Postman.json
│   ├── tests/
│   │   └── test_phocr_output.py
│   └── app/
│       ├── main.py
│       ├── mappingfinal.ipynb
│       ├── mappingfinal.py
│       ├── api/
│       │   └── ocr_controller.py
│       ├── dto/
│       │   └── models.py
│       ├── llm_integration/
│       │   └── llm.py
│       ├── ocr_modules/
│       │   └── modules.py
│       ├── services/
│       │   └── services.py
│       └── utils/
│           ├── image_utils.py
│           ├── pdf_utils.py
│           ├── quality_utils.py
│           └── test_utils.oy
│
├── frontend/
│   ├── package.json
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src/
│       ├── App.js
│       ├── App.css
│       ├── Ocr.js
│       ├── components/
│       │   ├── batch/
│       │   │   └── BatchResults.js
│       │   ├── common/
│       │   │   ├── ErrorDisplay.js
│       │   │   ├── FormField.js
│       │   │   └── TabButton.js
│       │   ├── detection/
│       │   │   ├── ConfidenceOverlay.js
│       │   │   └── EnhancedConfidenceOverlay.js
│       │   ├── multipage/
│       │   │   ├── MultipageExtraction.js
│       │   │   └── PageNavigation.js
│       │   ├── results/
│       │   │   └── UnifiedMultipageResults.js
│       │   ├── tabs/
│       │   │   ├── ExtractionTab.js
│       │   │   ├── HandwritingTab1.js
│       │   │   ├── MultiImageResults.js
│       │   │   ├── UnifiedResultsComponent.js
│       │   │   └── VerificationTab.js
│       │   ├── upload/
│       │   │   ├── CameraCapture.js
│       │   │   └── FileUploadArea.js
│       │   └── verification/
│       │       ├── DataEntryForm.js
│       │       └── VerificationResults.js
│       ├── constants/
│       │   ├── fields.js
│       │   └── styles.js
│       ├── hooks/
│       │   ├── useBatchOCR.js
│       │   ├── useCamera.js
│       │   ├── useFileUpload.js
│       │   ├── useFormData.js
│       │   ├── useMultiImageOCR.js
│       │   ├── useMultipageOCR.js
│       │   ├── useMultipagePdf.js
│       │   ├── useOCRDetection.js
│       │   ├── useOCRExtraction.js
│       │   ├── useUnifiedExtraction.js
│       │   └── useVerification.js
│       └── utils/
│           ├── apiService.js
│           └── errorHandling.js
```




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
 ### Here is the [link](https://youtu.be/L9iFKjycY8Q) for full setup video of our solution.
git clone https://github.com/KrishnaChaitanya16/MosipDecode2025.git
### Backend Setup

#### Option A: (Without Docker)
For developers who want to run and modify the code directly.

**Prerequisites:**
- Python 3.10+
- pip
- Node.js (v18+) & npm
- Git
- Docker (optional, for containerized deployment)

**Installation:**
1. Clone the repository:
  ```bash
  git clone https://github.com/KrishnaChaitanya16/MosipDecode2025.git
  cd SE_LAB_PROJECT
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
5. (Optional) Set up Ollama for LLM integration:
  - Download and install [Ollama](https://ollama.com/download)
  - Verify installation:
    ```bash
    ollama --version
    ```
  - Pull the Qwen2.5 model:
    ```bash
    ollama pull qwen2.5:1.5b
    ollama list
    # Ensure 'qwen2.5:1.5b' appears in the list
    ```
6. Start the LLM server (in backend/app):
  ```bash
  cd app
  python mappingfinal.py
  ```
7. In a new terminal, activate the virtual environment and start the FastAPI backend:
  ```bash
  cd backend
  .venv\Scripts\activate  # (if not already activated)
  uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  ```

#### Option B: (With Docker)
For quick setup or deployment.

1. Ensure Docker is installed and running.
2. Pull the prebuilt image:
  ```bash
  docker pull venkat96r/ocr_backend:latest
  docker run -d -p 8000:8000 venkat96r/ocr_backend:latest
  ```
3. Or build the image locally:
  ```bash
  docker build -t ocr_backend:latest .
  docker run -d -p 8000:8000 ocr_backend:latest
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


**Without building the image locally**:
	
	docker pull venkat96r/ocr_backend:latest
	
	
After the pull is you should see something like this:

- Run the image :
	
	``` 
	docker run -d -p 8000:8000 venkat96r/ocr_backend:latest
	```
After the successful run you should see something like this:

**If you want to build the image locally**:

Navigate to the root directory and run the follwoing command:

``` bash
docker build -t ocr_backend:latest .
```
To run the image:

``` bash
docker run -d -p 8000:8000 ocr_backend:latest
```

















	
	
			
	
	

       


		
	




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

 
   
