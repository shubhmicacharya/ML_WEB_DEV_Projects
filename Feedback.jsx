import React, { useEffect, useState } from "react";

export default function Feedback() {
  const [scores, setScores] = useState([]);
  const [postureScore, setPostureScore] = useState(null);

  useEffect(() => {
    const savedScores = JSON.parse(localStorage.getItem("feedback_scores")) || [];
    const savedPosture = localStorage.getItem("posture_score") || null;

    setScores(savedScores);
    setPostureScore(savedPosture);
  }, []);

  return (
    <div className="feedback-container" style={{ padding: "20px" }}>
      <h2>Interview Feedback</h2>

      <h3>Posture Score</h3>
      <p>{postureScore !== null ? postureScore : 0}</p>

      <h3>Answer Scores</h3>
      {scores.length === 0 ? (
        <p>0</p>
      ) : (
        <ul>
          {scores.map((score, index) => (
            <li key={index}>
              Question {index + 1}: {score === 0 ? "No answer detected (0 score)" : score}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
