import React, { useState, useEffect } from 'react';
import axios from 'axios';


const ModelDetails = () => {
    const [modelDetails, setModelDetails] = useState({});

    useEffect(() => {
        // Fetch data from the API when the component mounts
        fetchModelDetails();
    }, []);

    const fetchModelDetails = async () => {
        try {
            const response = await axios.get('/model_details');
            setModelDetails(response.data);
        } catch (error) {
            console.error('Error fetching model details:', error);
        }
    };

    // Render the model details
    return (
        <div>
            <h1>Model Details</h1>
            <pre>{JSON.stringify(modelDetails, null, 2)}</pre>
        </div>
    );
};

export default ModelDetails;
