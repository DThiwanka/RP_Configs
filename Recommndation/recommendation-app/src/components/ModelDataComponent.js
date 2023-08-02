import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ModelDataComponent = () => {
    const [modelData, setModelData] = useState(null);

    useEffect(() => {
        // Function to fetch model data from the API
        const fetchModelData = async () => {
            try {
                const response = await axios.get('/model_data');
                setModelData(response.data);
            } catch (error) {
                console.error('Error fetching model data:', error);
            }
        };

        fetchModelData();
    }, []);

    return (
        <div>
            {modelData ? (
                <div>
                    <h2>Model Data</h2>
                    <p>Feature Names: {JSON.stringify(modelData.feature_names)}</p>
                    <p>Target Variable: {modelData.target_variable}</p>
                    <p>Number of Data Points: {modelData.num_data_points}</p>
                </div>
            ) : (
                <p>Loading model data...</p>
            )}
        </div>
    );
};

export default ModelDataComponent;
