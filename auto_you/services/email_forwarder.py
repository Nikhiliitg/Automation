# services/email_forwarder.py
from typing import List
from tools.gmail_tool import GmailTool

class EmailForwarder:
    def __init__(self):
        self.gmail = GmailTool()

    def forward_matching_emails(self,
        sender_email: str,
        keywords: List[str],
        forward_to: str,
        max_results: int = 10) -> int:
        results = self.gmail.service.users().messages().list(
            userId='me',
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        forwarded_count = 0

        for msg in messages:
            msg_data = self.gmail.service.users().messages().get(
                userId='me', id=msg['id']
            ).execute()

            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])
            subject = self.gmail._get_header(headers, "Subject")
            sender_raw = self.gmail._get_header(headers, "From")
            sender_actual = self.gmail._extract_email(sender_raw)

            if sender_actual.lower() == sender_email.lower():
                if any(k.lower() in subject.lower() for k in keywords):
                    self.gmail.forward_email(msg['id'], forward_to)
                    forwarded_count += 1

        return forwarded_count
