// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar({ username, onLoginClick, onSignOut }) {
  return (
    <nav className="navbar navbar-expand-lg bg-white shadow-sm px-4">
      <div className="container-fluid">
        <Link className="navbar-brand text-primary fw-bold" to="/">
          <i className="fas fa-robot me-2"></i>AI Interview
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul className="navbar-nav d-flex align-items-center">
            <li className="nav-item">
              <Link className="nav-link" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/upload">Upload Resume</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/interview">Interview</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/feedback">Feedback</Link>
            </li>
            
          </ul>
        </div>
      </div>
    </nav>
  );
}
