from flask import Flask, jsonify, request
from getEmailInfo import process_new_email 
from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from datetime import date
from bson.objectid import ObjectId
from flask_cors import CORS
from google.cloud import pubsub_v1
from threading import Thread

app = Flask(__name__)

# Enable cross origin resource sharing backend/frontend to communicate
CORS(app)

load_dotenv()
print(f"MONGO_URI: {os.getenv('MONGO_URI')}")
uri = os.getenv("MONGO_URI")
#app.config["MONGO_URI"] = os.getenv("MONGO_URI")
#mongo = PyMongo(app)

def listen_for_messages():
    project_id = 'internshipwebapp'
    subscription_id = 'email-sub'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data}")
        message.ack()
        # Call the email processing function
        with app.app_context():
            process_new_email()

    print(f"Listening for messages on {subscription_path}...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()  # Blocks and listens indefinitely
    except Exception as e:
        print(f"Listening interrupted: {e}")
        streaming_pull_future.cancel()  # Stop the pull loop



# Database connection
def get_db_connection():
    client = MongoClient(uri)
    db = client['statuxdb']
    collection = db['internships']
    return db

@app.route('/api/search', methods=['GET'])
def search_internships():
    company_name = request.args.get('company', '')
    
    # Ensure the database connection is established
    db = get_db_connection()

    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    # Perform a case-insensitive search in the database
    results = db.internships.find({
        'company': {'$regex': f'^{company_name}', '$options': 'i'}  # Case-insensitive match
    })

    # Format the results into a list
    internships = [{
        "id": str(internship["_id"]),
        "company": internship["company"],
        "position": internship["position"],
        "status": internship["status"],
        "date_applied": internship["date_applied"]
    } for internship in results]

    return jsonify(internships), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "App is running!"})

# Run the pull listener in a separate thread
def run_pull_listener():
    listen_for_messages()

    
@app.route('/api/internships', methods=['GET'])
def get_internships():
    db = get_db_connection()
    print("Received request for /api/internships")  # Debug log
    internships = list(db.internships.find().sort("_id", -1))
    for internship in internships:
        internship['_id'] = str(internship['_id'])
    
    return jsonify(internships)

@app.route('/api/internships', methods=['POST'])
def add():
    conn = get_db_connection()
    data = request.json
    try:
        internship = {
            'company': data.get('company'),
            'position': data.get('position'),
            'status': data.get('status'),
            'date_applied': data.get('date_applied', str(date.today()))
        }
        result = conn.internships.insert_one(internship)
        return jsonify({'message': 'Internship added successfully', 'id': str(result.inserted_id)})
    except Exception as e:
        return jsonify({'message': f'Error adding internship: {e}'})
    
@app.route('/api/internships/<string:internship_id>', methods=['DELETE'])
def delete_internship(internship_id):
    print(f"internship_id: {internship_id}")
    conn = get_db_connection()
    conn.internships.delete_one({'_id': ObjectId(internship_id)})
    return jsonify({'message': 'Internship deleted successfully'})

@app.route('/api/internships/<string:internship_id>', methods=['PUTT'])
def update_app_status(internship_id, new_status):
    conn = get_db_connection()
    data = request.json
    try:
        result = conn.internships.update_one(
            {'_id': ObjectId(internship_id)},
            {'$set': {'status': new_status}}
        )
        if result.matched_count > 0:
            
            print(f"Updated internship {internship_id} to {new_status}")
        else:
            print(f"Internship {internship_id} not found")
    except Exception as e:
        print(f"Error updating internship: {e}")

#load machine learning model vectorizer and classifier from disk

                        
if __name__ == '__main__':
    listener_thread = Thread(target=run_pull_listener, daemon=True)
    listener_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=8080, debug=True)
