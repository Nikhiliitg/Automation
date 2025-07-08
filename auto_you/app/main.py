import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.gmail_tool import GmailTool
from db.database import create_db_and_tables
create_db_and_tables()


def send_email_interactive():
    print("\n✉️ Let's send an email!\n")
    to = input("📧 Enter recipient email: ").strip()
    subject = input("📝 Enter subject: ").strip()
    print("💬 Enter body (end with Ctrl+D on Linux/Mac or Ctrl+Z then Enter on Windows):")
    body = ""

    try:
        while True:
            line = input()
            body += line + "\n"
    except EOFError:
        pass

    g = GmailTool()
    result = g.send_email(to, subject, body)
    print("\n✅ Email sent successfully!")
    print("📬 Message ID:", result.get("id", "N/A"))

def fetch_unread_emails():
    g = GmailTool()
    print("\n📥 Fetching unread emails...\n")
    mails = g.fetch_unread_emails()
    for i, m in enumerate(mails, start=1):
        print(f"📧 Email {i}")
        print("From   :", m['from'])
        print("Subject:", m['subject'])
        print("Summary:", m['summary'])
        print("-" * 50)

if __name__ == "__main__":
    print("=== Nikhil’s Gmail LLM Bot ===")
    print("1️⃣  Read unread emails")
    print("2️⃣  Send a new email")
    choice = input("👉 Choose an option [1/2]: ").strip()

    if choice == "1":
        fetch_unread_emails()
    elif choice == "2":
        send_email_interactive()
    else:
        print("❌ Invalid choice. Run again.")