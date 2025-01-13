from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for
from getEmailInfo import get_emails, analyze_email, extract_company, extract_position, decode_body
import pickle
from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from datetime import date
from bson.objectid import ObjectId

app = Flask(__name__)
load_dotenv()
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")


uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

db = client['statuxdb']
collection = db['internships']

try:
    result = collection.insert_one({
        "company": "Tech Corp",
        "position": "Backend Developer Intern",
        "status": "OA",
        "date_applied": "2025-01-09"
    })
    print(f"Document inserted with ID: {result.inserted_id}")
except Exception as e:
    print(f"Error: {e}")