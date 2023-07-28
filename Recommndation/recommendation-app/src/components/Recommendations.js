import React, { useState } from 'react';
import '../css/Recommendations.css';

function Recommendations() {
  const [userID, setUserID] = useState('');
  const [age, setAge] = useState('');
  const [fashion_types, setFashionTypes] = useState([]);
  const [most_common_words, setMostCommonWords] = useState([]);
  const [most_recommended_age, setMostRecommendedAge] = useState('');
  const [outfit_choices, setOutfitChoices] = useState([]);
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
      setFashionTypes(data.fashion_types);
      setMostCommonWords(data.most_common_words);
      setMostRecommendedAge(data.most_recommended_age);
      setOutfitChoices(data.outfit_choices);
      setRecommendations(data.recommendations);
      setError('');
    } catch (error) {
      setError(error.message);
      setAge('');
      setFashionTypes([]);
      setMostCommonWords([]);
      setMostRecommendedAge('');
      setOutfitChoices([]);
      setRecommendations([]);
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
        {most_recommended_age && <p>Most Recommended Age: {most_recommended_age}</p>}

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

        {most_common_words.length > 0 && (
          <div>
            <h2>Most Common Words:</h2>
            <ul>
              {most_common_words.map((word, index) => (
                <li key={index}>{word}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {outfit_choices.length > 0 && (
        <div className="outfit-choices">
          <h2>Outfit Choices:</h2>
          <ul>
            {outfit_choices.map((outfit, index) => (
              <li key={index}>{outfit}</li>
            ))}
          </ul>
        </div>
      )}

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
