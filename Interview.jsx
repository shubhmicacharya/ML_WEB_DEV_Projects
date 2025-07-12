import React, { useEffect, useState, useRef } from 'react';
import '../App.css';
import axios from 'axios';

// Simulated posture scoring function (replace with your actual posture detection logic)
const getPostureScore = (videoElement) => {
  // Placeholder: random score between 70 and 100
  // You can run your pose detection on videoElement here and calculate a real score
  return Math.floor(70 + Math.random() * 30);
};

const evaluateAnswers = async (userAnswers, standardAnswers, postureScore, candidateName) => {
  try {
    const response = await axios.post("http://localhost:7001/evaluate", {
      answers: userAnswers,
      standard_answers: standardAnswers,
      posture_score: postureScore,
      candidate_name: candidateName
    });

    const scores = response.data.feedback_scores;
    localStorage.setItem("feedback_scores", JSON.stringify(scores));
    localStorage.setItem("posture_score", postureScore);
    return scores;
  } catch (error) {
    console.error("Error evaluating answers:", error);
    return [];
  }
};


export default function Interview() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [displayedQuestion, setDisplayedQuestion] = useState("");
  const videoRef = useRef(null);
  const [videoOn, setVideo] = useState(false);
  const [text, setText] = useState("");
  const [listening, setListening] = useState(false);
  const [candidateName, setCandidateName] = useState("");
  const [userAnswers, setUserAnswers] = useState([]);

  useEffect(() => {
    const storedQuestions = JSON.parse(localStorage.getItem("questions") || "[]");
    if (storedQuestions.length === 0) return;
    const shuffled = storedQuestions.sort(() => 0.5 - Math.random());
    const selected = shuffled.slice(0, 5);
    setQuestions(selected);
  }, []);

  useEffect(() => {
  if (questions.length === 0) return;

  setDisplayedQuestion(questions[0]);
  setText("");
  
  let index = 0;
  const answers = [];

  const interval = setInterval(() => {
    answers.push(text);

    index += 1;
    if (index < questions.length) {
      setDisplayedQuestion(questions[index]);
      setText("");
    } else {
      clearInterval(interval);

      const standardAnswerMap = {
        "What are your strengths?": "My strengths include adaptability, communication, and problem-solving skills.",
        "Tell me about your projects.": "I have worked on several projects including an AI-based interview system and an OCR-based text reader.",
        "Why should we hire you?": "You should hire me because I am passionate, driven, and aligned with your company values.",
        "What are your weaknesses?": "One of my weaknesses is public speaking, but I am working to improve it through practice.",
        "Tell me about yourself.": "I am a recent graduate with a background in software engineering and a passion for building impactful tech solutions."
      };

      const standardAnswers = questions.map(q => standardAnswerMap[q] || "");

      const postureScore = getPostureScore(videoRef.current);

      // Replace empty answers with "0"
      const sanitizedAnswers = answers.map(ans => (ans && ans.trim() !== "") ? ans : "0");

      evaluateAnswers(sanitizedAnswers, standardAnswers, postureScore, candidateName).then(() => {
        alert("Interview Completed !!");
        window.location.href = "/feedback";
      });
    }
  }, 10000);

  return () => clearInterval(interval);
}, [questions]);



  useEffect(() => {
    if (!videoOn) {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
      return;
    }

    navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error("Error accessing webcam:", err);
      });
  }, [videoOn]);

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  const recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  const startListening = () => {
    setListening(true);
    recognition.start();

    recognition.onresult = (event) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        transcript += event.results[i][0].transcript;
      }
      setText(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event);
    };
  };

  const stopListening = () => {
    setListening(false);
    recognition.stop();
  };

  useEffect(() => {
    const name = localStorage.getItem("candidate_name");
    if (name) setCandidateName(name);
  }, []);

  return (
    <>
      <p style={{ fontSize: "1.2rem", fontWeight: "bold", marginBottom: "20px" }}>
        Welcome, {candidateName}!
      </p>

      <p style={{ fontSize: "1.2rem", fontWeight: "bold", marginBottom: "20px" }}>
        For each question you will get 10 seconds to answer
      </p>

      <div className="interview-container">
  <div className="question-box">
    <h3>Question</h3>
    <p>{displayedQuestion || "Loading question..."}</p>
    <p>{text || ""}</p>
  </div>

  <div className="video-box">
    <h3>Video</h3>
    <video
      ref={videoRef}
      autoPlay
      muted
      playsInline
    />
  </div>
</div>


      <div className="mictoggle">
        {listening ? (
          <button onClick={stopListening}>
            <i className="fa-solid fa-microphone-slash"></i>
          </button>
        ) : (
          <button onClick={startListening}>
            <i className="fa-solid fa-microphone"></i>
          </button>
        )}
      </div>

      <div className="vidtoggle">
        {videoOn ? (
          <button onClick={() => setVideo(false)}>
            <i className="fa-solid fa-video-slash"></i>
          </button>
        ) : (
          <button onClick={() => setVideo(true)}>
            <i className="fa-solid fa-video"></i>
          </button>
        )}
      </div>
    </>
  );
}
