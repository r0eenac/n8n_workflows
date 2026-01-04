# 📖 Setup & Usage Instructions

This guide will walk you through setting up the Python Decryption Worker and configuring the n8n workflow.

## 📂 1. Project Structure
Ensure all files are located in a single directory on your server/computer:

```text
/pdf-decryptor-project
│
├── app.py                # Flask server logic
├── Dockerfile            # Container build instructions
├── requirements.txt      # Python dependencies (flask, pikepdf)
├── workflow.json         # n8n workflow file
└── INSTRUCTIONS.md       # This file
```

🐳 2. Setting up the Python Worker (Docker)
We will run the Python script as a Docker container. This acts as a microservice that accepts encrypted files and returns them unlocked.

Step A: Build the Image
Open a terminal in the project folder and run:

Bash

docker build -t pdf-decryptor .

Step B: Run the Container
Run the container and expose it on port 5000. (If you use Docker Compose or Portainer, configure it to restart automatically).

Bash

docker run -d \
  --name pdf-worker \
  --restart unless-stopped \
  -p 5000:5000 \
  pdf-decryptor
Verify it's running: Run docker logs pdf-worker to ensure the server is listening.




⚡ 3. n8n Configuration
Step A: Import the Workflow
Open n8n.

Create a new workflow.

Click the menu (three dots top-right) -> Import from File.

Select workflow.json.

Step B: Re-connect Credentials
The workflow is imported with placeholder credentials.

Open every Google Drive node (there are 4 of them).

Go to the Credentials tab.

Select your actual Google Drive account from the list.

Step C: Environment Variables (Security)
To avoid hardcoding sensitive data, set the following environment variables in your n8n instance (via .env file or Docker settings):


PDF_PASSWORD=your_actual_file_password
DECRYPTION_SERVICE_URL=http://INTERNAL_IP:5000/decrypt

⚠️ Important Network Note: If n8n is running in a Docker container, do not use localhost for the URL. Use the Internal IP of the host machine (e.g., 192.168.1.100) or the container name if they share a Docker network.



🚀 4. Execution & Testing
Source Data: Ensure you have encrypted PDF files in a source folder on Google Drive.

Folder ID: In the first node of the workflow (Search in folder), update the Folder ID to point to your source folder.

Run: Click Execute Workflow.

Monitor:

✅ Files are downloaded.

✅ Sent to the Python worker for decryption.

✅ Uploaded back to Drive into year-based folders (e.g., 2024, 2025).


⚠️ Troubleshooting
Connection Refused: n8n cannot reach the Python Worker. Check the DECRYPTION_SERVICE_URL. Ensure you are using the correct IP address (not localhost).

500 Internal Server Error: The decryption failed. This usually means the PDF_PASSWORD is incorrect or does not match the specific file.

Files upload to wrong location: Check the filename format. The Regex expects a year in the filename (e.g., Document_2024.pdf). Valid pattern: 202[0-9].
