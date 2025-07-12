from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk
from nltk.corpus import stopwords
from flask_pymongo import PyMongo

nltk.download('stopwords')

app = Flask(__name__)
STOPWORDS = set(stopwords.words('english'))
FILLER_WORDS = set(["um", "uh", "like", "you know", "so", "actually", "basically", "well"])

app.config["MONGO_URI"] = "mongodb://localhost:27017/interviewdb"
mongo = PyMongo(app)

def preprocess(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and t not in FILLER_WORDS]
    return " ".join(tokens)

def calculate_similarity(candidate_ans, expected_ans):
    candidate_clean = preprocess(candidate_ans)
    expected_clean = preprocess(expected_ans)

    if not candidate_clean or not expected_clean:
        return 0.0

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([candidate_clean, expected_clean])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(similarity * 100, 2)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    answers = data.get("answers", [])
    standard_answers = data.get("standard_answers", [])
    posture_score = data.get("posture_score", 0)
    candidate_name = data.get("candidate_name", "")

    # Simulated answer scoring (replace with actual logic)
    feedback_scores = [
        5 if ans != "0" else 0 for ans in answers
    ]

    # Store scores in MongoDB
    mongo.db.users.update_one(
        {"candidate_name": candidate_name},
        {
            "$set": {
                "feedback_scores": feedback_scores,
                "posture_score": posture_score
            }
        }
    )

    return jsonify({"feedback_scores": feedback_scores})

if __name__ == '__main__':
    app.run(debug=True)