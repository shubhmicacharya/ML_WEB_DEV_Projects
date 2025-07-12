import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function UploadResume() {
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [name, setName] = useState('');

  const handleFileChange = (e) => {
    setResume(e.target.files[0]);
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resume || !name) return alert("Please enter name and upload your resume.");

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("name", name);

    try {
      const response = await axios.post("http://127.0.0.1:7000/uploadResume", formData)

      const questions = response.data.questions;
      const resume_data= response.data.resume_data;

      localStorage.setItem("resume_data", JSON.stringify(resume_data));
      localStorage.setItem("questions", JSON.stringify(questions));
      localStorage.setItem("candidate_name", name);
      
      alert("Resume uploaded successfully!");
      navigate('/interview');
    } catch (error) {
      console.error(error);
      alert("Upload failed!");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="candidateName">Candidate Name</label>
        <input
          className="form-control"
          type="text"
          placeholder="Enter your name"
          value={name}
          onChange={handleNameChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="resumeUpload">Upload Resume (PDF only)</label>
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="form-control-file"
          required
        />
      </div>

      <button type="submit" className="btn btn-primary">Submit</button>
    </form>
  );
}
