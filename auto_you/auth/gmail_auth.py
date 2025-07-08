# auth/gmail_auth.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailAuth:
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def __init__(self, credentials_file="credentials.json", token_file="token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self.authenticate()

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
            creds = flow.run_local_server(port=50904)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def get_service(self):
        return self.service
