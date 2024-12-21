from flask import Flask, request, jsonify
from db_connection import get_db_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec

app = Flask(__name__)

@app.route('/match-jobs-tfidf', methods=['POST'])
def match_jobs_tfidf():
    try:
        data = request.get_json()
        if 'skills' not in data:
            return jsonify({'error': 'Skills field is required'}), 400

        user_skills = data['skills']

        # MongoDB connection
        db = get_db_connection()
        jobs_collection = db['jobs']
        jobs = list(jobs_collection.find())
        if not jobs:
            return jsonify({'message': 'No jobs found in the database', 'matched_jobs': []}), 404

        job_skills = [job['skills'] for job in jobs]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(job_skills + [user_skills])

        user_vector = tfidf_matrix[-1]
        similarities = cosine_similarity(user_vector, tfidf_matrix[:-1]).flatten()

        matched_jobs = []
        for i, similarity in enumerate(similarities):
            if similarity > 0.1:  # Adjust threshold as needed
                job = jobs[i]
                job['_id'] = str(job['_id'])
                job['similarity'] = similarity
                matched_jobs.append(job)

        matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)
        return jsonify({'message': 'Job matching completed', 'matched_jobs': matched_jobs}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/match-jobs-word2vec', methods=['POST'])
def match_jobs_word2vec():
    try:
        data = request.get_json()
        if 'skills' not in data:
            return jsonify({'error': 'Skills field is required'}), 400

        user_skills = data['skills'].split(', ')

        # MongoDB connection
        db = get_db_connection()
        jobs_collection = db['jobs']
        jobs = list(jobs_collection.find())
        if not jobs:
            return jsonify({'message': 'No jobs found in the database', 'matched_jobs': []}), 404

        # Train Word2Vec model on job skills
        job_skills = [job['skills'].split(', ') for job in jobs]
        model = Word2Vec(sentences=job_skills, vector_size=100, window=5, min_count=1, workers=4)

        matched_jobs = []
        for job in jobs:
            job_skills = job['skills'].split(', ')
            similarity = model.wv.n_similarity(user_skills, job_skills)
            if similarity > 0.1:  # Adjust threshold as needed
                job['_id'] = str(job['_id'])
                job['similarity'] = similarity
                matched_jobs.append(job)

        matched_jobs.sort(key=lambda x: x['similarity'], reverse=True)
        return jsonify({'message': 'Job matching completed', 'matched_jobs': matched_jobs}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Main entry point to run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
