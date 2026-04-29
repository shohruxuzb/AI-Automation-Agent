import time
import email.utils
from email_client import EmailClient
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, GEMINI_API_KEY, POLL_INTERVAL_SECONDS
import ai_agent

def extract_email_address(sender_string):
    """Extracts actual email address from strings like 'Name <email@exampl.com>'"""
    name, addr = email.utils.parseaddr(sender_string)
    return addr, name

def run_automation():
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD or not GEMINI_API_KEY:
        print("CRITICAL: Missing environment variables. Please check your .env file.")
        print("Expected:")
        print("- EMAIL_ADDRESS")
        print("- EMAIL_APP_PASSWORD")
        print("- GEMINI_API_KEY")
        return

    client = EmailClient()
    
    print("========================================")
    print("Starting AI Email Automation Agent...")
    print(f"Monitoring: {EMAIL_ADDRESS}")
    print("========================================")
    
    while True:
        try:
            client.connect()
            
            print("Checking for unread emails...")
            unread_emails = client.fetch_unread_emails()
            
            if not unread_emails:
                print("No new emails.")
            
            for eml in unread_emails:
                sender_addr, sender_name = extract_email_address(eml['sender'])
                
                # Ignore emails from ourselves
                if sender_addr == EMAIL_ADDRESS:
                    client.mark_as_read(eml['id'])
                    continue
                    
                print(f"\n--- Processing Email from: {sender_addr} ({sender_name}) ---")
                print(f"Subject: {eml['subject']}")
                
                # 1. Classify
                print("Thinking... 🤔")
                classification = ai_agent.classify_email(eml['subject'], eml['body'])
                print(f"Classification: {classification}")
                
                # 2. Generate Reply
                reply_text = ai_agent.generate_reply(eml['subject'], eml['body'], classification, sender_name)
                
                # 3. Send Reply
                if reply_text:
                    print(f"\nGenerating reply:\n{reply_text[:150]}...\n")
                    client.send_reply(sender_addr, eml['subject'], eml['message_id'], reply_text)
                    print("✅ Reply sent successfully.")
                else:
                    print("🚫 No reply generated (e.g. Spam).")
                
                # 4. Mark as read
                client.mark_as_read(eml['id'])
                print("✅ Email marked as read.")
                
            client.disconnect()
            
        except Exception as e:
            print(f"Error during execution cycle: {e}")
            try:
                client.disconnect()
            except Exception:
                pass
            
        print(f"\nWaiting {POLL_INTERVAL_SECONDS} seconds before next check...\n")
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_automation()
