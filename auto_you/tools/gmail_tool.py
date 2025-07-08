from auth.gmail_auth import GmailAuth
from llm.summarizer import Summarizer
import base64
import email
import re
from typing import List, Dict
from sqlmodel import Session
from db.models import EmailLog
from db.database import engine


class GmailTool:
    def __init__(self):
        self.service = GmailAuth().get_service()
        self.llm = Summarizer()

    def fetch_unread_emails(self, max_results=5) -> List[Dict[str, str]]:
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return [{"from": "", "subject": "No new emails", "summary": ""}]

            email_data = []

            with Session(engine) as session:
                for msg in messages:
                    msg_data = self.service.users().messages().get(
                        userId='me',
                        id=msg['id']
                    ).execute()

                    payload = msg_data.get('payload', {})
                    headers = payload.get('headers', [])
                    snippet = msg_data.get('snippet', "")

                    subject = self._get_header(headers, "Subject")
                    sender_raw = self._get_header(headers, "From")
                    sender_email = self._extract_email(sender_raw)
                    
                    sender_email = self._extract_email(sender_raw)

                    # ✅ Your new block goes HERE
                    priority_keywords = ["important", "referral", "opportunities"]
                    if sender_email.lower() == "nikhildeka20@gmail.com":
                        subject_lower = subject.lower()
                        if any(keyword in subject_lower for keyword in priority_keywords):
                            print(f"📤 Forwarding high-priority email from {sender_email} to nikhiliitg07@gmail.com")
                            self.forward_email(original_message_id=msg['id'], forward_to="nikhiliitg07@gmail.com")


                    # 🛑 Skip replying to yourself
                    if sender_email.lower() == "nikhildeka20@gmail.com":
                        print(f"⛔ Skipping self-sent email from {sender_email}")
                        continue

                    # 🛑 Skip known bot domains
                    blocked_domains = ["linkedin.com", "udemy.com", "angelbroking.in", "noreply", "sales", "no-reply", "updates"]
                    if any(d in sender_email.lower() for d in blocked_domains):
                        print(f"🔕 Skipping blocked sender: {sender_email}")
                        continue

                    # 🧠 Extract + summarize
                    body = self._extract_body(payload) or snippet
                    summary = self.llm.summarize(body)

                    email_data.append({
                        'from': sender_email,
                        'subject': subject,
                        'summary': summary
                    })

                    # 👋 Auto-reply if trigger words found
                    trigger_words = ["hi", "hit"]
                    content_to_check = (subject + " " + body).lower()
                    responded = any(word in content_to_check for word in trigger_words)

                    if responded:
                        print(f"👋 Auto-greeting triggered for: {sender_email}")
                        self.send_email(
                            to=sender_email,
                            subject="👋 Hey there!",
                            body="Thanks for reaching out! This is Nikhil’s Gmail AI bot here to greet you. Let me know if you need help!"
                        )

                    # 🗃️ Log email
                    email_log = EmailLog(
                        from_addr=sender_email,
                        subject=subject,
                        summary=summary,
                        responded=responded
                    )
                    session.add(email_log)

                    # ✅ Mark as read
                    self.service.users().messages().modify(
                        userId='me',
                        id=msg['id'],
                        body={'removeLabelIds': ['UNREAD']}
                    ).execute()

                session.commit()

            return email_data

        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []

    def send_email(self, to: str, subject: str, body: str) -> Dict:
        try:
            msg = email.message.EmailMessage()
            msg.set_content(body)
            msg['To'] = to
            msg['Subject'] = subject

            raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            create_message = {'raw': raw_msg}

            sent_message = self.service.users().messages().send(
                userId="me",
                body=create_message
            ).execute()

            return sent_message

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return {"error": str(e)}

    def _extract_body(self, payload) -> str:
        """Extract plain text body from multipart email payload."""
        try:
            parts = payload.get("parts")
            if parts:
                for part in parts:
                    if part.get("mimeType") == "text/plain":
                        data = part["body"].get("data")
                        if data:
                            return base64.urlsafe_b64decode(data).decode("utf-8")
            else:
                data = payload.get("body", {}).get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8")
        except Exception as e:
            print(f"⚠️ Failed to extract body: {e}")
        return ""

    def _extract_email(self, raw_sender: str) -> str:
        """Extract email address from 'Name <email>' format."""
        match = re.search(r'<(.+?)>', raw_sender)
        return match.group(1) if match else raw_sender.strip()

    def _get_header(self, headers: List[Dict], key: str) -> str:
        return next((h['value'] for h in headers if h['name'].lower() == key.lower()), f"No {key}")

    def forward_email(self, original_message_id: str, forward_to: str) -> dict:
        try:
            original = self.service.users().messages().get(
                userId='me',
                id=original_message_id,
                format='full'
            ).execute()

            payload = original.get("payload", {})
            body = self._extract_body(payload) or "📭 No content found"
            subject = self._get_header(payload.get("headers", []), "Subject")

            new_msg = email.message.EmailMessage()
            new_msg.set_content(body)
            new_msg['To'] = forward_to
            new_msg['Subject'] = f"[FWD] {subject}"
            new_msg['From'] = "me"  # Gmail will auto-fill this correctly

            raw_forward = base64.urlsafe_b64encode(new_msg.as_bytes()).decode()
            body = {'raw': raw_forward}

            sent = self.service.users().messages().send(
                userId="me", body=body
            ).execute()

            print(f"✅ Forwarded message ID {original_message_id}")
            return sent

        except Exception as e:
            print(f"❌ Failed to forward message: {e}")
            return {"error": str(e)}