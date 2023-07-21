import React, { useState } from 'react';
import '../css/DataInputForm.css';

const DataInputForm = () => {
  const [userData, setUserData] = useState({
    UserID: '',
    Age: '',
    Gender: '',
    FashionType: '',
    OutfitChoice: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setUserData({ ...userData, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('/insert_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      if (response.ok) {
        setSuccessMessage(data.message);
        setErrorMessage('');
        setUserData({
          UserID: '',
          Age: '',
          Gender: '',
          FashionType: '',
          OutfitChoice: '',
        });
        // Show alert confirmation
        alert('Data successfully submitted!');
      } else {
        setErrorMessage(data.error);
        setSuccessMessage('');
      }
    } catch (error) {
      setErrorMessage('Error occurred while submitting the data.');
      setSuccessMessage('');
    }
  };

  return (
    <div>
      <h2>Data Input Form</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {/* {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>} */}
      <form onSubmit={handleSubmit}>
        <label htmlFor="UserID">UserID:</label>
        <input
          type="text"
          id="UserID"
          name="UserID"
          value={userData.UserID}
          onChange={handleChange}
        />

        <label htmlFor="Age">Age:</label>
        <input
          type="text"
          id="Age"
          name="Age"
          value={userData.Age}
          onChange={handleChange}
        />

        <label htmlFor="Gender">Gender:</label>
        <input
          type="text"
          id="Gender"
          name="Gender"
          value={userData.Gender}
          onChange={handleChange}
        />

        <label htmlFor="FashionType">FashionType:</label>
        <input
          type="text"
          id="FashionType"
          name="FashionType"
          value={userData.FashionType}
          onChange={handleChange}
        />

        <label htmlFor="OutfitChoice">OutfitChoice:</label>
        <input
          type="text"
          id="OutfitChoice"
          name="OutfitChoice"
          value={userData.OutfitChoice}
          onChange={handleChange}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default DataInputForm;
