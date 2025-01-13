from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def reauthenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_591032654485-78cujvqj4l96u8glato5k64ojq1u3rnl.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("Token successfully refreshed")
    return creds

def get_credentials():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired:
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("Token successfully refreshed")
                except Exception as e:
                    print(f"Error refreshing token: {e}")
        else:
            creds = reauthenticate()
    return creds

def setup_email_watch():
    creds = get_credentials()
    try:
        service = build('gmail', 'v1', credentials=creds)
        watch_request = {
            'labelIds': ['INBOX'],
            'topicName': 'projects/internshipwebapp/topics/statux-4107'
        }
        service.users().watch(userId='me', body=watch_request).execute()
        print("Successfully set up email watch")
    except HttpError as error:
        print(f'An error occurred: {error}')

setup_email_watch()


