import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util

# Initialize pose detection and drawing tools
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize sentence similarity model
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

# Posture counters
Straight_counter = 0
Leaning_Left_counter = 0
Leaning_right_counter = 0
Slouching_counter = 0
Severely_Slouched_counter = 0
start_time = time.time()

# Interview Q&A dictionary
predefined_answers = {

    # HR-Based Questions
    "Tell me about yourself.": 
    "I am a computer science graduate with a strong interest in software development, data analytics, and machine learning. I have completed internships where I gained hands-on experience in Python programming and data analysis. I am passionate about solving real-world problems through technology.",

    "Why should we hire you?": 
    "You should hire me because I have a solid foundation in programming, data analysis, and problem-solving. I am a quick learner, a team player, and I am highly motivated to contribute to your company's success. My previous experiences have prepared me to take on challenging roles.",

    "What are your strengths and weaknesses?": 
    "My strengths include adaptability, problem-solving skills, and effective communication. I am also highly organized and pay attention to detail. One area I am working on improving is public speaking, but I have been attending workshops to overcome that.",

    "Where do you see yourself in 5 years?": 
    "In five years, I see myself in a leadership role, contributing to large-scale software projects, mentoring junior developers, and continuously learning new technologies. I aim to be a subject matter expert in data science and AI.",

    "Describe a challenging situation you faced and how you handled it.": 
    "During my final year project, we faced a major issue with integrating the backend and frontend due to API inconsistencies. I coordinated closely with my team, revised the API documentation, and reworked the code structure to resolve the issue. We successfully delivered the project on time.",

    "What are your salary expectations?": 
    "I am open to discussing a salary that aligns with industry standards and reflects my skills and experience. I am more focused on the opportunity for growth and learning within the role.",

    # Technical / Resume-Based Questions
    "Can you tell me more about your experience with Python from Languages?": 
    "I have been using Python for over 2 years, working on projects related to data analysis, web development with Flask, and machine learning. I am comfortable with libraries like pandas, NumPy, and scikit-learn.",

    "Can you tell me more about your experience with Pandas from Libraries?": 
    "I have used Pandas extensively for data manipulation and analysis. I have handled large datasets, performed data cleaning, and created meaningful insights through exploratory data analysis using Pandas.",

    "Can you tell me more about your experience with MySQL from Databases?": 
    "I have worked with MySQL to design and manage relational databases. In my internship, I developed optimized queries for data retrieval and managed the database schema to support a web-based application.",

    "Can you tell me more about your experience with Power BI from Data Analytics Tools?": 
    "I used Power BI to create interactive dashboards and reports. I worked on visualizing key performance indicators for business insights and automated reporting processes for faster decision-making.",

    "Can you tell me more about your experience with Git from Other Tools?": 
    "I have used Git for version control in all my team projects. I am familiar with branching strategies, pull requests, and resolving merge conflicts to maintain clean and collaborative codebases.",

    "Can you tell me more about your experience with Machine Learning from Areas of Interest?": 
    "I have built several machine learning models using scikit-learn and TensorFlow. I worked on classification, regression, and clustering problems and optimized model performance through hyperparameter tuning.",

    "Can you tell me more about your experience with Data Structures and Algorithms from Relevant Coursework?": 
    "I have a solid understanding of data structures like arrays, linked lists, stacks, queues, trees, and graphs. I have applied these concepts to solve algorithmic problems on platforms like LeetCode and HackerRank.",

    "Can you tell me more about your experience with Team Collaboration from Soft Skills?": 
    "In my internships and academic projects, I worked in teams where collaboration was key. I effectively communicated with team members, divided tasks, and ensured that we met deadlines while maintaining quality.",

    # Add more if needed...
}

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech(timeout_to_start=4, phrase_time_limit=4):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print(f"🎙️ Listening for your answer... (Start speaking within {timeout_to_start} seconds)")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=timeout_to_start, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("⏰ No answer detected within 4 seconds. Moving on...")
            return ""

    try:
        answer = recognizer.recognize_google(audio)
        print("✅ You said:", answer)
        return answer
    except sr.UnknownValueError:
        print("❗ Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("❗ Speech recognition service error.")
        return ""

# Calculate similarity
def calculate_similarity(user_answer, expected_answer):
    if not user_answer.strip():
        return 0.0
    embeddings = similarity_model.encode([user_answer, expected_answer], convert_to_tensor=True)
    similarity_score = util.cos_sim(embeddings[0], embeddings[1])
    return float(similarity_score)

# Feedback based on similarity score
def give_feedback(score):
    if score >= 0.8:
        return "Excellent answer!"
    elif score >= 0.5:
        return "Good, but can be improved."
    else:
        return "Try to give a more relevant answer."

# Posture angle calculation
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

# Posture detection function
def detect_posture(frame):
    global Straight_counter, Leaning_Left_counter, Leaning_right_counter, Slouching_counter, Severely_Slouched_counter, start_time
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape
    results = pose.process(frame_rgb)

    posture = "Unknown"
    color = (255, 255, 255)  # White

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        left_shoulder = [landmarks[11].x * w, landmarks[11].y * h]
        right_shoulder = [landmarks[12].x * w, landmarks[12].y * h]
        left_hip = [landmarks[23].x * w, landmarks[23].y * h]
        right_hip = [landmarks[24].x * w, landmarks[24].y * h]

        torso_angle = calculate_angle(left_shoulder, left_hip, right_hip)
        shoulder_diff = left_shoulder[1] - right_shoulder[1]

        if torso_angle > 160:
            posture = "Straight"
            color = (0, 255, 0)  # Green
            if time.time() - start_time >= 5:
                Straight_counter += 1
                start_time = time.time()

        elif 140 < torso_angle <= 160:
            if shoulder_diff > 20:
                posture = "Leaning Left"
                color = (255, 165, 0)  # Orange
                if time.time() - start_time >= 5:
                    Leaning_Left_counter += 1
                    start_time = time.time()

            elif shoulder_diff < -20:
                posture = "Leaning Right"
                color = (255, 165, 0)
                if time.time() - start_time >= 5:
                    Leaning_right_counter += 1
                    start_time = time.time()

            else:
                posture = "Slouching"
                color = (0, 0, 255)  # Red
                if time.time() - start_time >= 5:
                    Slouching_counter += 1
                    start_time = time.time()
        else:
            posture = "Severely Slouched"
            color = (0, 0, 128)  # Dark Red
            if time.time() - start_time >= 5:
                Severely_Slouched_counter += 1
                start_time = time.time()

        # Display posture status
        cv2.putText(frame, f"Posture: {posture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    return frame

# Start interview function with posture monitoring
def start_interview_with_posture_monitoring():
    print("\nStarting the predefined question interview with posture monitoring...\n")
    time.sleep(1)

    cap = cv2.VideoCapture(0)

    # Limit to 5 questions
    limited_questions = list(predefined_answers.items())[:5]

    for idx, (question, expected_answer) in enumerate(limited_questions, 1):
        print(f"\nQuestion {idx}: {question}")
        speak(question)

        question_start_time = time.time()
        answering = True

        # Loop while user answers the question and posture is monitored
        while answering:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from webcam.")
                break

            # Process posture
            frame = detect_posture(frame)

            # Display webcam frame
            cv2.imshow("Posture Monitoring", frame)

            # Check if time to get an answer
            if time.time() - question_start_time >= 2:  # Give a little time before answering
                user_answer = recognize_speech(timeout_to_start=4, phrase_time_limit=10)
                similarity = calculate_similarity(user_answer, expected_answer)
                feedback = give_feedback(similarity)

                print(f"Similarity Score: {similarity:.2f}")
                print(f"Feedback: {feedback}")
                speak(feedback)

                answering = False  # Move to next question after the answer

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Interview interrupted by user.")
                break

        print("Waiting 3 seconds before moving on...\n")
        time.sleep(3)

    cap.release()
    cv2.destroyAllWindows()

    print("\nInterview completed!")
    speak("Interview completed")

    # Speak posture summary
    print(f"Straight_counter: {Straight_counter}")
    engine.say(f"Detected Straight posture with {Straight_counter} counts")

    print(f"Leaning_Left_counter: {Leaning_Left_counter}")
    engine.say(f"Detected Leaning Left posture with {Leaning_Left_counter} counts")

    print(f"Leaning_right_counter: {Leaning_right_counter}")
    engine.say(f"Detected Leaning Right posture with {Leaning_right_counter} counts")

    print(f"Slouching_counter: {Slouching_counter}")
    engine.say(f"Detected Slouching posture with {Slouching_counter} counts")

    print(f"Severely_Slouched_counter: {Severely_Slouched_counter}")
    engine.say(f"Detected Severely Slouched posture with {Severely_Slouched_counter} counts")

    engine.runAndWait()


# Run
if __name__ == "__main__":
    start_interview_with_posture_monitoring()