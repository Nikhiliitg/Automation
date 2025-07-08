# app/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from sqlmodel import Session, select
from db.models import User, EmailLog
from db.database import create_db_and_tables, get_session
from tools.gmail_tool import GmailTool
from services.email_forwarder import EmailForwarder

app = FastAPI(title="Nikhil's Gmail AI Agent")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 📬 Model for POST /forward-emails
class ForwardRequest(BaseModel):
    sender_email: str
    keywords: List[str]
    forward_to: str
    max_results: int = 10

@app.post("/register-user")
def register_user(name: str, email: str, session: Session = Depends(get_session)):
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)

    GmailTool().send_email(
        to=email,
        subject="🎉 Welcome to Nik’s AI Inbox!",
        body=f"Hi {name}, you’ve just been registered with Nikhil’s AI Gmail bot. You’ll now be auto-greeted if you email me!"
    )

    return {"msg": "User registered and greeted!", "user_id": user.id}

@app.get("/")
def index():
    return {"message": "👋 Welcome to Nikhil's Gmail AI Agent"}

@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.get("/emails/unread")
def fetch_and_greet(session: Session = Depends(get_session)):
    emails = GmailTool().fetch_unread_emails()

    for e in emails:
        email_log = EmailLog(
            from_addr=e['from'],
            subject=e['subject'],
            summary=e['summary'],
            responded="hi" in e['summary'].lower() or "hit" in e['subject'].lower()
        )
        session.add(email_log)

    session.commit()
    return {"fetched": len(emails), "emails": emails}

@app.get("/email-logs")
def get_logs(session: Session = Depends(get_session)):
    return session.exec(select(EmailLog)).all()

# 🔥 NEW: Modular Forwarding Endpoint
@app.post("/forward-emails")
def forward_emails(req: ForwardRequest):
    forwarder = EmailForwarder()
    count = forwarder.forward_matching_emails(
        sender_email=req.sender_email,
        keywords=req.keywords,
        forward_to=req.forward_to,
        max_results=req.max_results
    )
    return {"message": f"✅ Forwarded {count} email(s)."}
