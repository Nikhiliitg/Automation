# 📨 AI Gmail Agent — The Self-Driving Inbox Bot 🤖📬

> A fully automated Gmail bot that reads, replies, forwards, and summarizes emails using Python, Gmail API, Hugging Face Transformers, and FastAPI — all running **100% locally with zero cloud cost**.

---

## 🚀 Features

- 📬 Reads unread Gmail messages
- 🧠 Summarizes content using HuggingFace LLMs
- 👋 Auto-replies to greetings like "Hi" or "Hello"
- 📤 Auto-forwards mails with "Important", "Referral", or "Opportunity" in subject
- 🗂️ Stores all activity in a SQLite database
- 🧠 Runs autonomously every 5 minutes using APScheduler
- 🌐 Includes a FastAPI server + Swagger UI for optional manual use
- 🆓 100% local — No EC2, no Render, no GCP charges (Pocket Friendly🥲)

---

## 🧱 Tech Stack

| Layer        | Tool               |
|--------------|--------------------|
| 📬 Email API | Gmail API (OAuth2) |
| 🧠 NLP       | HuggingFace Transformers (`facebook/bart-large-cnn`) |
| 🧠 Logic     | Custom Python logic |
| ⚙️ Scheduler | APScheduler         |
| 🌐 API       | FastAPI (with Swagger) |
| 🛢️ Database  | SQLite + SQLModel   |

---

## 🔧 Setup Instructions

```bash
git clone https://github.com/Nikhiliitg/Automation
cd auto_you

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# 🔐 Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable Gmail API
3. Configure OAuth consent screen → Add yourself as a test user
4. Create OAuth Client → Download `client_secret.json`
5. Rename it to `credentials.json` and put it in the project root

---

## 🧠 Run the Bot (Automation Starts Instantly)

```bash
uvicorn app.main:app --reload
```

✅ FastAPI server starts  
✅ APScheduler runs every 5 minutes  
✅ `GmailTool` fetches unread → replies, forwards, logs  
✅ No clicks required. Just works.

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## ⚙️ Trigger Logic

| Condition | Action |
|----------|--------|
| Subject contains `Important`, `Referral`, or `Opportunities` | 🔁 Auto-forwards to your main email |
| Body contains `hi` or `hello` | 🤖 Sends a friendly greeting reply |
| Sender is spam/noreply | 🚫 Skipped |
| Anything else | 🧠 Summarized and logged |

---

## 🛠️ Optional API Endpoints

| Route | Description |
|--------|-------------|
| `/emails/unread` | Manually fetch + respond to unread mails |
| `/forward-emails` | Manually forward with custom filters |
| `/email-logs` | View all email actions logged |
| `/register-user` | Register user and send greeting |
| `/users` | List registered users |

---

## 🧠 How It Works (Under the Hood)

- `gmail_tool.py`: Handles auth, fetching, replying, forwarding
- ` summarizer.py `: Summarize and Sanitize the mails Content With HF Models
- `scheduler.py`: Triggers job every 5 minutes (APScheduler (not used yet))
- `email_forwarder.py`: Modular forwarding logic
- `database.py` + `models.py`: SQLModel-powered SQLite DB
- `fast_api.py`: FastAPI app with startup automation
-  ` main.py ` : Runs in your Local Machine and see results in Terminal 
---

## 💡 Architecture

```
Startup ▶️ Scheduler runs every 5 min
       └── GmailTool ▶️ Fetch unread
           ├── Summarize
           ├── Auto-greet
           ├── Auto-forward
           └── Log to DB
```

---

## 💬 Why Not Real-Time Gmail Pub/Sub?

Because this project is:

- 💰 Cost-free (no EC2, no Cloud Run)
- 🧱 Local dev friendly
- 🧠 Still powerful with 5-min interval automation

You can add Gmail Watch + Pub/Sub later if needed.

---

## 🔮 Next Ideas

- Use GPT to classify job/referral mail
- Attach resume to auto-replies
- Build a dashboard with Streamlit
- Deploy to cloud with real-time trigger

---

## 📁 Project Structure

```
auto_you/
├── app/
|   └── init.py 
│   └── main.py            # local running
|   └── fast_api.py 
├── auth/
|    └── secrets.py            #credentials from gmail.api   
|    └── paths.py 
├── config/
|    └── gmail_auth.py 
├── tools/
│   └── gmail_tool.py      # Core bot logic
├── services/
│   └── email_forwarder.py # Modular forwarder
├── db/
│   ├── database.py
│   └── models.py
|__ llm/
│   ├── summarizer.py
├── scheduler.py           # APScheduler trigger
├── credentials.json       # OAuth2 client file
└── README.md              # You’re here
└── generate_structure.py
```

---

## 📚 Credits

- HuggingFace 🤗 Transformers  
- Gmail API  
- FastAPI + Uvicorn  
- SQLModel by Tiangolo (SQLAlchemy 2.0 interface)

---

## 📣 Built With ❤️ by

**Nikhil Deka**  
AI Engineer • Python Dev • 🧙‍♂️  
Connect on [LinkedIn](https://linkedin.com/in/nikhildeka/)

> ⭐ Star this repo if you love automation.  
> 🛠️ Fork it to build your own inbox empire.

> 😜 Any Startup/ MNC , if you like the idea please contact me [Gmail](nikhiliitg07@gmail.com)