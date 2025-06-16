
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3001;

app.use(cors()); // Allow CORS for Grafana

const sensorDataHistory = [];

// 🔁 Run initial prediction on server startup
const initPython = spawn('python', ['-u', 'main.py']);
initPython.stdout.on('data', (data) => {
    const output = data.toString().trim();
    console.log(` ${output}`);

    try {
        const prediction = JSON.parse(output); // Only parses valid JSON
        sensorDataHistory.push(prediction);
    } catch (err) {
        // Skip non-JSON logs like "Running predictions..." or status messages
    }

});
initPython.stderr.on('data', (err) => {
    console.error(`Initial Python Error: ${err}`);
});
initPython.on('close', (code) => {
    console.log(`🔚 Initial Python script exited with code ${code}`);
});

/*

// 📡 Endpoint for Grafana JSON API to fetch predictions
app.get('/sensor-data', (req, res) => {
    const python = spawn('python', ['-u', 'main.py']);
    let output = '';

    python.stdout.on('data', (data) => {
        const text = data.toString();
        output += text;
        console.log(`🐍 Python Output: ${text.trim()}`);
    });

    python.stderr.on('data', (err) => {
        console.error(`❌ Python Error: ${err}`);
    });

    python.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: 'Prediction script failed' });
        }

        const predictions = {};
        const lines = output.trim().split('\n');

        lines.forEach(line => {
            const match = line.match(/Predicted (\w+) for next step: ([\d.]+)/);
            if (match) {
                predictions[match[1]] = parseFloat(match[2]);
            }
        });

        const result = {
            time: new Date().toISOString(),
            predictions
        };

        console.log("📊 Final Prediction JSON:", result);
        res.json(result);
    });
});
*/

// Optional: redirect root `/` to `/predict`
app.get('/sensor-data', (req, res) => {
    res.setHeader("Content-Type", "application/json");
    res.status(200).json(sensorDataHistory); // Serve all stored prediction outputs
});

// 🚀 Start the serverS
app.listen(PORT, () => {
    console.log(`✅ Server running at http://localhost:${PORT}`);
});