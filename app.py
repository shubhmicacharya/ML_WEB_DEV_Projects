from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from resume_parser import extract_info_from_resume
from question_generator import generate_questions
from flask_pymongo import PyMongo


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["MONGO_URI"] = "mongodb://localhost:27017/interviewdb"
mongo = PyMongo(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/uploadResume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files or 'name' not in request.form:
        return jsonify({"error": "Missing data"}), 400

    resume = request.files['resume']
    name = request.form['name']
    filename = secure_filename(resume.filename)

    # Save file locally
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    # Extract data (placeholder, adjust as needed)
    questions = ["What are your strengths?", "Tell me about your projects?"]
    resume_data = {"skills": ["Python", "ML"], "education": "B.Tech CSE"}

    # Store user info in MongoDB
    mongo.db.users.insert_one({
        "candidate_name": name,
        "resume_filename": filename
    })

    return jsonify({
        "questions": questions,
        "resume_data": resume_data
    })
    
@app.route('/submit_interview', methods=['POST'])
def submit_interview():
    data = request.json
    candidate_name = data.get('candidate_name')
    posture_score = data.get('posture_score')
    question_score = data.get('question_score')

    if not candidate_name:
        return jsonify({'error': 'Candidate name required'}), 400

    ##save_interview_result(candidate_name, posture_score, question_score)
    return jsonify({'message': 'Interview data saved successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=7000)
