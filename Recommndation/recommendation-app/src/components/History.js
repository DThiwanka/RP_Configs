import React, { useState, useEffect } from 'react';
import axios from 'axios';

const History = () => {
    const [trainingHistory, setTrainingHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Function to fetch the training history data from the API
        const fetchTrainingHistory = async () => {
            try {
                const response = await axios.get('/get_training_history');
                setTrainingHistory(response.data.training_history);
            } catch (error) {
                console.error('Error fetching training history:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchTrainingHistory();
    }, []);

    return (
        <div>
            <h2>Training History</h2>
            {isLoading ? (
                <p>Loading...</p>
            ) : trainingHistory.length > 0 ? (
                <ul>
                    {trainingHistory.map((accuracy, index) => (
                        <li key={index}>Model {index + 1} Accuracy: {accuracy.toFixed(4)}</li>
                    ))}
                </ul>
            ) : (
                <p>No training history available.</p>
            )}
        </div>
    );
};

export default History;
