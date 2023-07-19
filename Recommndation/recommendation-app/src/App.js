import React from 'react';
import { BrowserRouter as Router, Link, Routes, Route } from 'react-router-dom';
import Recommendations from './Recommendations';

function Home() {
  return (
    <div>
      <h1>Welcome to Outfit Recommendations</h1>
      <Link to="/recommendations">
        <button>Recommendations</button>
      </Link>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/recommendations">Recommendations</Link>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recommendations" element={<Recommendations />} />
      </Routes>
    </Router>
  );
}

export default App
