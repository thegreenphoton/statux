import os
import base64
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import spacy
import pickle
from bson.objectid import ObjectId
from ml_model import extract_name_from_custom_nlp
from flask import jsonify, current_app
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
load_dotenv()
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
uri = os.getenv("MONGO_URI")


def get_db_connection():
    client = MongoClient(uri)
    db = client['statuxdb']
    collection = db['internships']
    return db

def setup_email_watch():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if creds and creds.expired:
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("Token successfully refreshed")
                except Exception as e:
                    print(f"Error refreshing token: {e}")
        else:
            creds = reauthenticate()

        try:
            service = build('gmail', 'v1', credentials=creds)
            watch_request = {
                'labelIds': ['INBOX'],
                'topicName': 'projects/statux-327617/topics/email'
            }
            service.users().watch(userId='me', body=watch_request).execute()
            print("Successfully set up email watch")
        except HttpError as error:
            print(f'An error occurred: {error}')

last_history_id = None


def process_new_email():
    with current_app.app_context():
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        else:
            creds = reauthenticate()
        try:
            service = build('gmail', 'v1', credentials=creds)

            # Fetch the most recent email
            results = service.users().messages().list(userId='me', maxResults=1).execute()
            messages = results.get('messages', [])

            if messages:
                message = messages[0]
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                payload = msg.get('payload', {})
                body = get_body(payload)

                if body:
                    db = get_db_connection()
                    vectorizer, classifier = load_model()
                    features = vectorizer.transform([body])
                    is_confirmation = classifier.predict(features)[0]
                    print(f"Is confirmation: {is_confirmation}")
                    if False:
                    #if is_confirmation == 'confirmation':
                        company_name = extract_name_from_custom_nlp(body)
                        position = extract_position(body)

                        if company_name and position:
                            
                            db.internships.insert_one({
                                'company': company_name,
                                'position': position,
                                'status': 'Applied',
                                'date_applied': date.today().isoformat()
                            })
                            print(f"added {company_name} for {position}")
                    else:
                        company, position, status = analyze_email(body)
                        if company and (position or status):
                            if position != "other" and status != 'Unknown':
                                internship = db.internships.find_one({
                                    'company': {'$regex': f'^{company}$', '$options': 'i'},
                                    'position': {'$regex': f'^{position}$', '$options': 'i'}
                                })
                                if internship:
                                    internship_id = internship['_id']
                                    result = db.internships.update_one(
                                        {'_id': ObjectId(internship_id)},
                                        {'$set': {'status': status}}
                                    )
                                    if result.matched_count > 0:
                                        print(f"Updated internship {internship_id} to {status}")
                                else:
                                    print(f"Internship {internship_id} not found")
                                
            return jsonify({'message': 'Emails processed and statuses updated!'})
                    
        except HttpError as error:
            print(f'An error occurred: {error}')
        except Exception as e:
            print(f"Error updating internship: {e}")

def get_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            if mime_type == 'text/plain':
                data = part['body'].get('data', '')
                text = base64.urlsafe_b64decode(data).decode('utf-8')
                return text
            elif mime_type == 'text/html':
                data = part['body'].get('data', '')
                html = base64.urlsafe_b64decode(data).decode('utf-8')
                # Optionally, strip HTML tags to get plain text
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                return text
            elif mime_type.startswith('multipart/'):
                # Recursively process nested parts
                return get_body(part)
    else:
        data = payload.get('body', {}).get('data', None)
        if data:
            mime_type = payload.get('mimeType', '')
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            if mime_type == 'text/plain':
                return decoded_data
            elif mime_type == 'text/html':
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(decoded_data, 'html.parser')
                text = soup.get_text()
                return text
    return None

nlp = spacy.load("en_core_web_sm")

def is_base64(s):
    try: 
        return base64.b64.encode(base64.b64decode(s)) == s.encode('utf-8')
    except Exception:
        return False

def fix_base64_padding(data):
    missing_padding = len(data) % 4
    if missing_padding: 
        data += '=' * (4 - missing_padding)
    return data

def decode_body(body):
    if isinstance(body, bytes):
        try:
            body = body.decode('utf-8')
            print(f"Successfully decoded body as utf-8")
                   
        except (UnicodeDecodeError, base64.binascii.Error, ValueError) as e:
            print(f"Failed to decode body as utf-8: {e}")
            return None

    if isinstance(body, bytes):
        print(f"Body is still bytes, possibly binary data, skipping further processing")
        return None
    
    if isinstance(body, str) and is_base64(body):
        try:
            body = fix_base64_padding(body)
            body = base64.urlsafe_b64decode(body).decode('utf-8')
        except (UnicodeDecodeError, base64.binascii.Error, ValueError) as e:
            print(f"Failed to decode body: {e}")
            return None
        
    if not isinstance(body, str):
        print(f"Error: body is not a string: {type(body)}")
        return None
    
    print(f"successfully decoded body")
    return body

def analyze_email(body): 
    #uses spacy to process the email body
    new_body = decode_body(body)

    doc = nlp(new_body)

    position = extract_position(new_body)
    position = position.strip().lower() if position else None

    company = extract_company(new_body)
    company = company.strip().lower() if company else None

    print(f"Extracted company: {company} and position: {position}")
    #keyword-based approach to detect status
    if any(keyword in doc.text.lower() for keyword in ['unfortunetely', 'other candidates', 'other applicants', 'thank you for your interest', 'have decided not', 'we wont be able to', 'at this time', 'we regret', 'after careful consideration', 'you have not']):
        status = "Denied"
    elif any(keyword in doc.text.lower() for keyword in ['congratulations', 'we are pleased', 'offer']):
        status = "Position Offered"
    elif any(keyword in doc.text.lower() for keyword in ['assessment', 'interview', 'schedule', 'invite', 'invited', 'challenge', 'hackerrank']):
        status = "OA"
    else:
        status = "Unknown"

    print(f"Determined status: {status}")
    return company, position, status
    
def extract_company(body):

    conn = get_db_connection()
    companies = conn.internships.distinct('company')

    extracted_company = None
    for company in companies:
        if company.lower() in body.lower():
            print(f"company found: '{company}'")
            extracted_company = company
            break

    if extracted_company == None:
        doc = nlp(body)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                extracted_company = ent.text
                break

    return extracted_company

def extract_position(body):
    doc = nlp(body)
    position = None

    db = get_db_connection()
    positions = db.internships.distinct('position')
    
    position = None
    for job_title in positions:
        if job_title.lower() in doc.text.lower():
            print(f"position found: '{position}'")
            position = job_title
            break 
    return position

def reauthenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_591032654485-78cujvqj4l96u8glato5k64ojq1u3rnl.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)
    print("Token file missing. Please authenticate your app.")

    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    return creds

def load_model():
    with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)
    with open('email_classifier.pkl', 'rb') as model_file:
        classifier = pickle.load(model_file)
    return vectorizer, classifier




