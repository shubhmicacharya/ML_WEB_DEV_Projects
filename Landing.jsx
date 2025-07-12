// src/pages/Landing.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';



export default function Landing() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  const handleGetStarted = () => {
    navigate('/upload');
  };

  const handleLogin = (name) => {
    setUsername(name);
  };

  const handleLogout = () => {
    setUsername('');
  };

  return (
    <>

      <div className="landing text-center py-5">
        <h1>Welcome to the AI Interview Assistant</h1>
        <p>Your journey to acing interviews starts here!</p>
        <p>Upload your resume and get personalized interview questions.</p>
        <button className="btn btn-primary mt-3" onClick={handleGetStarted}>
          Get Started
        </button>
      </div>
    </>
  );
}
