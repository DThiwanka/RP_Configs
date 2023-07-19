import React, { useState } from 'react';

const Recommendations = () => {
  const [userID, setUserID] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  const handleUserIDChange = (event) => {
    setUserID(event.target.value);
  };

const handleFormSubmit = async (event) => {
  event.preventDefault();

  try {
    const response = await fetch('http://localhost:5000/recommendations', {
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
      setRecommendations(data.recommendations);
      setError('');
    } catch (error) {
      setError(error.message);
      setRecommendations([]);
    }
  };

  return (
    <div>
      <h1>Outfit Recommendation System</h1>
      <form onSubmit={handleFormSubmit}>
        <label htmlFor="userID">User ID:</label>
        <input
          type="text"
          id="userID"
          value={userID}
          onChange={handleUserIDChange}
        />
        <button type="submit">Get Recommendations</button>
      </form>

      {error && <p>{error}</p>}

      {recommendations.length > 0 && (
        <div>
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
};

export default Recommendations;
