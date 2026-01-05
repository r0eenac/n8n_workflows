# 🔖 Linkwarden AI Bookmark Manager
### Smart automation for saving and categorizing links in Linkwarden using AI

This project contains an **n8n workflow** that acts as an intelligent "brain" for bookmarking. It receives a URL, scrapes its content, and uses an LLM (OpenAI/Gemini) to decide whether to save the link into an existing Linkwarden collection or automatically create a new one based on the context. Finally, it sends a confirmation via WhatsApp.

---


<img width="1024" height="572" alt="image" src="https://github.com/user-attachments/assets/f36ff3d4-a256-4fc6-9a13-91b703a0e608" />

## 🚀 Features

* **🕵️ Metadata Extraction:** Automatically visits the URL and extracts the page title, description, and main content.
* **🤖 AI Categorization:** Uses an AI Agent (LangChain) to analyze the content and match it against your *existing* Linkwarden collections.
* **📂 Dynamic Collection Management:**
    * If a matching category exists → Saves the link there.
    * If NO match is found → **Creates a new collection** in Linkwarden and saves the link.
* **🔗 Linkwarden API Integration:** Full interaction with self-hosted Linkwarden instances.
* **📱 WhatsApp Notifications:** Sends a formatted summary (Name, Description, Category) via GreenAPI upon success.

---

## 🛠️ Prerequisites

To run this workflow, you need:

1.  **n8n:** Self-hosted or Cloud instance.
2.  **Linkwarden:** A running instance (Self-hosted). You must generate an **API Token** in your settings.
3.  **AI Credential:** An API Key for OpenAI (GPT-4/3.5) or Google Gemini.
4.  **GreenAPI:** An active account for sending WhatsApp messages (Instance ID + Token).

---

## ⚙️ Configuration

After importing the JSON file into n8n, you must update the placeholder values to match your environment:

### 1. Update API Endpoints & Tokens
The workflow uses placeholder values for security. Please update the following Nodes:

* **HTTP Requests (Linkwarden):**
    * There are 4 HTTP nodes. Change the URL from `http://192.168.x.x:3000` to your actual Linkwarden server address.
    * In the `Header Parameters` -> `Authorization`, replace `Bearer Token` with your actual token (Format: `Bearer eyJ...`).
* **AI Model:**
    * Ensure the OpenAI or Google Gemini credential is selected and connected.
* **WhatsApp (GreenAPI):**
    * Select your GreenAPI credential.
    * Update the `chatId` field to your destination phone number (Format: `123456789@g.us`).

### 2. Workflow Inputs
This workflow is designed as a **Sub-workflow**. It expects to be triggered by another workflow (e.g., a WhatsApp Router) with the following input:
* `chatInput`: The URL string to be saved.

---

## 🧠 Logic Flow

1.  **Trigger:** Receives a URL from a parent workflow.
2.  **Scraping:** Fetches the HTML of the target page and extracts metadata.
3.  **Fetch Context:** Retrieves a list of *all* current collections from Linkwarden.
4.  **AI Decision:**
    * The Agent analyzes the Page Content vs. Existing Collections.
    * **Decision:** Returns either `use_existing` (with ID) or `create_new` (with Name/Description).
5.  **Routing (Switch):**
    * **➡️ Existing:** Cleans the URL and POSTs the link to the chosen Collection ID.
    * **➡️ New:** Creates a new Collection via API -> Gets the new ID -> POSTs the link.
6.  **Notification:** Sends a success message to WhatsApp.

---

## 🛡️ Security Note

* The provided JSON file has been sanitized (IPs and Tokens removed).
* If your n8n and Linkwarden are on the same internal network, you can use local IPs (as shown in the placeholders).
* **Recommendation:** Use n8n Credentials or Environment Variables for sensitive tokens instead of hardcoding them in the HTTP nodes.
