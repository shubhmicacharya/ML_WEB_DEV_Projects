import logo from './logo.svg';
import './App.css';
import React from 'react';
//import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UploadResume from './components/UploadResume';
import Interview from './components/Interview';
import Feedback from './components/Feedback';
import Navbar from './components/Navbar';
import Landing from './components/Landing';

function App() {
  const username = "Candidate"; // Replace this later with actual dynamic data

  return (
    <Router>
      <Navbar username={username} />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/upload" element={<UploadResume />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/feedback" element={<Feedback />} />
      </Routes>
    </Router>
  );
}

export default App;
