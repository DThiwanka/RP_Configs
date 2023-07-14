const express = require('express');
const csv = require('csv-parser');
const fs = require('fs');
const { spawn } = require('child_process');
const app = express();

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', './views');

// Define the route to render the index view
app.get('/', (req, res) => {
    res.render('index', { prediction: null });
});

// Define the route to handle form submission and make predictions
app.get('/predict', (req, res) => {
    const id = req.query.id;
    const age = req.query.age;

    // Read the existing data from the CSV file
    const existingData = [];
    fs.createReadStream('../existing_data.csv')
        .pipe(csv())
        .on('data', (row) => {
            existingData.push(row);
        })
        .on('end', () => {
            // Prepare the input data
            const inputData = [...existingData, { ID: id, Age: age }];
            const inputDataJson = JSON.stringify(inputData);

            // Call the Python script to make predictions
            const pythonProcess = spawn('python', ['predict.py'], { stdio: 'pipe' });

            pythonProcess.stdin.write(inputDataJson);
            pythonProcess.stdin.end();

            pythonProcess.stdout.on('data', (data) => {
                const prediction = data.toString().trim();
                res.render('index', { prediction });
            });

            pythonProcess.stderr.on('data', (data) => {
                const errorMessage = data.toString();
                if (errorMessage.includes("ImportError: cannot import name 'joblib'")) {
                    console.error(errorMessage);
                    res.status(500).send('An error occurred. Please check the Python dependencies.');
                } else {
                    console.error(errorMessage);
                    res.status(500).send('An error occurred.');
                }
            });
        });
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});