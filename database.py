import sqlite3
from datetime import datetime

DB_NAME = 'interview_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            interview_time TEXT NOT NULL,
            posture_score REAL,
            question_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_interview_result(candidate_name, posture_score, question_score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    interview_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO interview_results (candidate_name, interview_time, posture_score, question_score)
        VALUES (?, ?, ?, ?)
    ''', (candidate_name, interview_time, posture_score, question_score))
    conn.commit()
    conn.close()
