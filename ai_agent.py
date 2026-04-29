import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

def classify_email(email_subject: str, email_body: str) -> str:
    """Classifies the email intent using Gemini."""
    prompt = f"""
You are an intelligent email assistant. Analyze the incoming email and classify its primary intent.
Return ONLY ONE of the following categories:
- Support Query
- Sales Lead
- Meeting Request
- Spam
- Other

Email Subject: {email_subject}

Email Body:
{email_body}

Classification:"""
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        classification = response.text.strip()
        
        valid_classifications = ["Support Query", "Sales Lead", "Meeting Request", "Spam", "Other"]
        # Basic validation
        for valid in valid_classifications:
            if valid.lower() in classification.lower():
                return valid
                
        return "Other"
    except Exception as e:
        print(f"Error classifying email: {e}")
        return "Other"

def generate_reply(email_subject: str, email_body: str, classification: str, sender_name: str = "there") -> str:
    """Generates a professional reply based on the email content and classification."""
    
    if classification == "Spam":
        return "" # Do not reply to spam
        
    prompt = f"""
You are an expert AI email assistant acting on my behalf. Draft a professional, friendly, and concise reply to the following email.
The email was classified as: {classification}.

Do not include sender placeholders like [Your Name], sign it as 'AI Assistant'. Be helpful.

Email Subject: {email_subject}
Email Body (from {sender_name}):
{email_body}

Draft Reply:"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating reply: {e}")
        return ""
