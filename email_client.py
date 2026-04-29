import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, IMAP_SERVER, SMTP_SERVER, SMTP_PORT

class EmailClient:
    def __init__(self):
        self.imap = None
        self.smtp = None
        
    def connect(self):
        """Establish IMAP and SMTP connections."""
        print(f"Connecting to {IMAP_SERVER}...")
        self.imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        self.imap.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        
        print(f"Connecting to {SMTP_SERVER}...")
        self.smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.smtp.starttls()
        self.smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        print("Connected successfully.")

    def disconnect(self):
        """Close connections."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except Exception:
                pass
        if self.smtp:
            self.smtp.quit()
            self.smtp = None
            
    def _decode_string(self, text, charset):
        if isinstance(text, bytes):
            return text.decode(charset or 'utf-8', errors='ignore')
        return text
            
    def fetch_unread_emails(self):
        """Fetches unread emails from the inbox."""
        self.imap.select("INBOX")
        status, response = self.imap.search(None, 'UNSEEN')
        
        unread_msg_ids = response[0].split()
        emails = []
        
        for msg_id in unread_msg_ids:
            status, msg_data = self.imap.fetch(msg_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Extract Subject
                    subject = "No Subject"
                    subject_header = decode_header(msg["Subject"])[0]
                    if subject_header[0]:
                        subject = self._decode_string(subject_header[0], subject_header[1])

                    # Extract Sender
                    sender = msg.get("From", "Unknown Sender")
                    message_id_header = msg.get("Message-ID", "")
                    
                    # Extract Body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" not in content_disposition and content_type == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                                except Exception:
                                    pass
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = msg.get_payload(decode=True).decode('utf-8', 'ignore')
                            except Exception:
                                pass
                                
                    emails.append({
                        "id": msg_id,
                        "subject": subject,
                        "sender": sender,
                        "body": body,
                        "message_id": message_id_header
                    })
        return emails
        
    def mark_as_read(self, msg_id):
        """Marks a specific email as read."""
        self.imap.select("INBOX")
        self.imap.store(msg_id, '+FLAGS', '\\Seen')
        
    def send_reply(self, to_email: str, subject: str, in_reply_to_id: str, reply_body: str):
        """Sends an email reply."""
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = f"Re: {subject}" if not subject.lower().startswith('re:') else subject
        
        if in_reply_to_id:
            msg['In-Reply-To'] = in_reply_to_id
            msg['References'] = in_reply_to_id

        msg.attach(MIMEText(reply_body, 'plain'))
        
        self.smtp.send_message(msg)
