import pymongo

def get_db_connection():
    # Replace the URI with your MongoDB URI
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["job_database"]  # Use your database name
    return db

