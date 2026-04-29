# AI Email Automation Agent 🚀

A Python-based AI assistant that automatically monitors a Gmail inbox, categorizes incoming emails, and securely drafts context-aware replies using Google's Gemini LLM. It's built as a background daemon utilizing real-time IMAP/SMTP standard email interfaces—meaning you don't have to fiddle with complex Google Cloud OAuth screens for simple automation tasks.

## Features ✨
- **IMAP Connection:** Securely polls for unread emails every 30 seconds.
- **AI Classification:** Detects if an email is a "Support Query", "Sales Lead", "Spam", "Meeting Request", or "Other".
- **Intelligent Replies:** Generates a professional, contextual reply to the thread based on the category using Gemini API (`gemini-2.5-flash`).
- **Spam Filtering:** Automatically ignores any email flagged as Spam.
- **Zero Duplicate processing:** Marks handled emails as Read (Seen) ensuring you don't reply multiple times.

---

## Setup & Installation 🛠️

### 1. Clone & Install
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials (`.env`)
You need to duplicate the `.env.example` file, name it `.env`, and provide your values.
```bash
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
GEMINI_API_KEY=your_gemini_api_key
```

**⚠️ Important Setup Notes:**
*   **Gmail App Password**: You *cannot* use your primary Google Account password. You must generate an App Password. 
    *   Enable 2-Step Verification in your Google Account settings.
    *   Navigate to **Security -> 2-Step Verification -> App passwords**.
    *   Generate a new password and ensure you **remove the spaces** when pasting it into your `.env` file!
*   **Gemini API Key**: Grab a free API key over at [Google AI Studio](https://aistudio.google.com/).

### 3. Run the Automation
Start the daemon from your terminal. It will continuously monitor your inbox.
```bash
python main.py
```

## How It Works ⚙️
1. The script uses the standard built-in `imaplib` library to login to `imap.gmail.com`.
2. It fetches the text body of any emails marked `UNSEEN`.
3. The email context is pushed to the `google-generativeai` package to extract categories and formulate a response.
4. Using `smtplib`, it binds the AI generated reply with the `In-Reply-To` and `References` headers and dispatches it straight back to the sender.  

---
*Created as part of the AI Automation showcase!*
