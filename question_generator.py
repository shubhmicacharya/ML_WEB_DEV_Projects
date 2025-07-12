def generate_questions(resume_data):
    keywords = resume_data.get("keywords", [])
    questions = []

    for skill in keywords:
        questions.append(f"Can you explain your experience with {skill}?")

    # Add general HR questions
    questions += [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Describe a challenging project you worked on.",
        "Why do you want to join our company?",
        "Where do you see yourself in 5 years?"
    ]

    return questions
