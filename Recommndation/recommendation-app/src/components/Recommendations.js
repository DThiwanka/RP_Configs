import React, { useState } from 'react';
import '../css/Recommendations.css';

function Recommendations() {
  const [userID, setUserID] = useState('');
  const [age, setAge] = useState('');
  const [fashion_types, setfashion_types] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  const handleUserIDChange = (event) => {
    setUserID(event.target.value);
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch('/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userID }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
      }

      const data = await response.json();
      setAge(data.age);
      setRecommendations(data.recommendations);
      setfashion_types(data.fashion_types);
      setError('');
    } catch (error) {
      setError(error.message);
      setAge('');
      setRecommendations([]);
      setfashion_types([]);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Outfit Recommendation System</h1>
      <form onSubmit={handleFormSubmit} className="form">
        <label htmlFor="userID" className="label">
          Enter User ID:
        </label>
        <input
          type="text"
          id="userID"
          value={userID}
          onChange={handleUserIDChange}
          className="input"
        />
        <button type="submit" className="button">
          Get Recommendations
        </button>
      </form>

      <div className="user-details">
        <h2>User Details</h2>
        {error && <p className="error">{error}</p>}
        {age && <p>Age: {age}</p>}

        {fashion_types.length > 0 && (
          <div>
            <h2>Fashion Types Bought:</h2>
            <ul>
              {fashion_types.map((fashionType, index) => (
                <li key={index}>{fashionType}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {recommendations.length > 0 && (
        <div className="recommendations">
          <h2>Recommended Outfit Choices:</h2>
          <ul>
            {recommendations.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Recommendations;