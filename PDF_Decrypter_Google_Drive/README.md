# 🔓 Automated PDF Batch Decryptor & Organizer
Batch process encrypted PDF files via Google Drive

This project contains an n8n workflow that automates the handling of encrypted PDF files. The system scans a source folder, downloads the files, sends them to an external service for decryption, and uploads the unlocked versions back to Google Drive, automatically organizing them into sub-folders based on the year extracted from the filename.

> **Important:** This service requires a python microserver running on docker, and does not use any external APIs to avoid sending any sensitive info outside.


<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/937ca3bd-5a1e-477b-b59d-03be899b6d08" />

## 🚀 Features
* **📂 Batch Processing:** Automatically iterates over files in a specific Google Drive folder.
* **🔐 Decryption:** Removes password protection using an external Python microservice.
* **📅 Intelligent Sorting:** Extracts the year from the filename using Regex (e.g., `202[0-9]`).
* **📁 Dynamic Folder Creation:** Checks if a destination folder for the specific year exists; if not, it creates it automatically.
* **☁️ Organized Upload:** Uploads the decrypted file to the correct destination folder.

## 🛠️ Prerequisites
To run this workflow, you need:
* **n8n:** Self-hosted or Cloud instance.
* **Google Drive Credentials:** OAuth2 connection with Read/Write permissions.
* **Decryption Worker:** A simple internal microservice (Python) that accepts POST requests to decrypt files.
    * **Endpoint:** `/decrypt`
    * **Method:** `POST`
    * **Payload:** `multipart/form-data` (requires `file` and `password`).

## ⚙️ Configuration
After importing the JSON, configure the following values to match your environment:

### 1. Environment Variables (Recommended)
For security, avoid hardcoding sensitive data. Set these in your n8n environment:
* `PDF_PASSWORD`: The master password for the encrypted files.
* `DECRYPTION_SERVICE_URL`: The internal URL of your worker (e.g., `http://python-worker:5000/decrypt`).

### 2. Workflow Nodes
* **Google Drive Nodes:** Re-connect your specific credential.
* **HTTP Request:** Update the URL and Password fields (or use the expressions linked to the env variables above).
* **Source Folder:** In the first Search node, define the ID of the folder you want to monitor.

## 🧠 Logic Flow
1.  **Trigger:** Manual execution.
2.  **Search:** Lists files in the source directory.
3.  **Loop:** Iterates through files one by one:
    * **📥 Download:** Fetches the encrypted file binary.
    * **🔓 Decrypt:** Sends binary + password to the worker; receives clean binary.
    * **🗓️ Regex Match:** Extracts the year (e.g., `Doc_2024_01.pdf` -> `2024`).
    * **📂 Folder Check:** Queries Drive for a folder named "2024".
        * If exists: Returns ID.
        * If missing: Creates new folder and returns new ID.
    * **📤 Upload:** Saves the clean file to the target folder.

## 📦 Python Worker Example
The workflow expects a backend service to handle the actual decryption. Below is a minimal Flask example:

```python
from flask import Flask, request, send_file
import pikepdf
import io

app = Flask(__name__)

@app.route('/decrypt', methods=['POST'])
def decrypt_pdf():
    # Retrieve password and file from the request
    password = request.form.get('password')
    uploaded_file = request.files['file']
    
    # Process the PDF
    pdf = pikepdf.open(uploaded_file, password=password)
    
    # Save decrypted version to memory
    output_stream = io.BytesIO()
    pdf.save(output_stream)
    output_stream.seek(0)
    
    return send_file(output_stream, mimetype='application/pdf', as_attachment=True, download_name='decrypted.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
