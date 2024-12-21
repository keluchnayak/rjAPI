from flask import Flask, jsonify
from db_connection import get_db_connection

app = Flask(__name__)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    # Get the database connection
    db = get_db_connection()
    jobs_collection = db['jobs']  # Collection where job data is stored
    
    # Retrieve all job listings from the MongoDB collection
    jobs = list(jobs_collection.find({}, {'_id': 0}))  # Exclude MongoDB's default _id field
    
    # Return the job listings in JSON format
    return jsonify({'jobs': jobs}), 200

if __name__ == "__main__":
    app.run(debug=True)
