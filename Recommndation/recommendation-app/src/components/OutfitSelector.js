import React, { useState } from 'react';

const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
};

const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '350px',
    padding: '20px',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
};

const labelStyle = {
    fontWeight: 'bold',
    marginTop: '10px',
};

const inputStyle = {
    width: '100%',
    padding: '8px',
    marginTop: '5px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
};

const selectStyle = {
    width: '100%',
    padding: '8px',
    marginTop: '5px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '14px',
};

const buttonStyle = {
    marginTop: '10px',
    padding: '10px 20px',
    border: 'none',
    borderRadius: '4px',
    backgroundColor: '#007bff',
    color: '#fff',
    fontSize: '16px',
    cursor: 'pointer',
};

const successMessageStyle = {
    color: '#007bff',
    fontWeight: 'bold',
    marginTop: '10px',
};

const fashion_choices = {
    "Casual Streetwear": [
        "Denim jeans, a graphic T-shirt, and sneakers",
        "Hoodie, leggings, and athletic shoes",
        "Distressed jeans, oversized hoodie, and sneakers"
    ],
    "Bohemian/Boho Chic": [
        "Flowy maxi dress and sandals",
        "Floral sundress and wedges",
        "Embroidered peasant top, flared jeans, and wedges"
    ],
    "Vintage-inspired": [
        "High-waisted pants, a blouse, and heels",
        "Polka dot swing dress, cat-eye sunglasses, and slingback heels",
        "Crochet top, flared pants, and platform sandals"
    ],
    "Minimalist": [
        "A-line skirt, tucked-in blouse, and ballet flats",
        "Cuffed chinos, a polo shirt, and loafers",
        "Flowy culottes, a structured top, and mules"
    ],
    "Preppy": [
        "Tailored blazer, trousers, and oxford shoes",
        "Plaid skirt, cashmere sweater, and pointed-toe flats",
        "Tailored jumpsuit, statement necklace, and stiletto pumps"
    ],
    "Edgy/Rock-inspired": [
        "Leather jacket, band T-shirt, ripped jeans, and ankle boots",
        "Plaid shirt, leather pants, combat boots, and spikes",
        "Leather biker jacket, striped tee, skinny jeans, and boots"
    ],
    "Athleisure": [
        "Athletic leggings, sports bra, and sneakers",
        "Track pants, hoodie, and trainers",
        "Sports shorts, tank top, and running shoes"
    ],
    "Glamorous": [
        "Sequin gown, statement earrings, and high heels",
        "Silk slip dress, faux fur coat, and strappy sandals",
        "Form-fitting cocktail dress, statement clutch, and stiletto heels"
    ]
    // Add more fashion types and outfit choices here
};

const OutfitSelector = () => {
    const [user_id, setUser_id] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('Male');
    const [fashion_type, setFashion_type] = useState('');
    const [outfit_choice, setOutfit_choice] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const handleFormSubmit = (event) => {
        event.preventDefault();
        fetch('/insert_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                UserID: parseInt(user_id),
                Age: parseInt(age),
                Gender: gender,
                FashionType: fashion_type,
                OutfitChoice: outfit_choice,
            }),
        })
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to save outfit.');
                }
            })
            .then((data) => {
                setSuccessMessage('Outfit saved successfully!');
                setUser_id('');
                setAge('');
                setGender('Male');
                setFashion_type('');
                setOutfit_choice('');
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };


    return (
        <div style={containerStyle}>
            <h1>Fashion Outfit Selector</h1>
            <form style={formStyle} onSubmit={handleFormSubmit}>
                <label style={labelStyle} htmlFor="user_id">User ID:</label>
                <input style={inputStyle} type="text" id="user_id" value={user_id} onChange={(e) => setUser_id(e.target.value)} required />

                <label style={labelStyle} htmlFor="age">Age:</label>
                <input style={inputStyle} type="text" id="age" value={age} onChange={(e) => setAge(e.target.value)} required />

                <label style={labelStyle} htmlFor="gender">Gender:</label>
                <select style={selectStyle} id="gender" value={gender} onChange={(e) => setGender(e.target.value)}>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>

                <label style={labelStyle} htmlFor="fashion_type">Select Fashion Type:</label>
                <select style={selectStyle} id="fashion_type" value={fashion_type} onChange={(e) => setFashion_type(e.target.value)} required>
                    <option value="" disabled>Select a fashion type</option>
                    {Object.keys(fashion_choices).map((key) => (
                        <option key={key} value={key}>{key}</option>
                    ))}
                </select>

                {fashion_type && (
                    <>
                        <label style={labelStyle} htmlFor="outfit_choice">Select Outfit Choice:</label>
                        <select style={selectStyle} id="outfit_choice" value={outfit_choice} onChange={(e) => setOutfit_choice(e.target.value)} required>
                            <option value="" disabled>Select an outfit choice</option>
                            {fashion_choices[fashion_type].map((choice, index) => (
                                <option key={index} value={choice}>{choice}</option>
                            ))}
                        </select>
                    </>
                )}

                <button style={buttonStyle} type="submit">Save Outfit</button>
            </form>

            {successMessage && <p style={successMessageStyle}>{successMessage}</p>}
        </div>
    );
};

export default OutfitSelector;
