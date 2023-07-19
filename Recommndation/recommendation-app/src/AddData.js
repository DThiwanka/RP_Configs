import React, { useState } from 'react';

function AddData() {
  const [userID, setUserID] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [fashionType, setFashionType] = useState('');
  const [outfitChoice, setOutfitChoice] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    // Create a new data object to send to the API
    const newData = {
      UserID: userID,
      Age: age,
      Gender: gender,
      FashionType: fashionType,
      OutfitChoice: outfitChoice,
    };

    // Send the data to the API endpoint to add to the CSV
    fetch('/addData', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the API
        console.log(data); // For example, you can log the response
        // Reset the form
        setUserID('');
        setAge('');
        setGender('');
        setFashionType('');
        setOutfitChoice('');
      })
      .catch((error) => {
        // Handle errors
        console.error(error);
      });
  };

  return (
    <div>
      <h1>Add Data</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="userID">User ID:</label>
        <input
          type="text"
          id="userID"
          value={userID}
          onChange={(event) => setUserID(event.target.value)}
        />

        {/* Add other form fields for age, gender, fashion type, and outfit choice */}

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default AddData;
