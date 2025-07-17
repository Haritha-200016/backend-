const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = 3001;

app.use(cors());

const sensorDataHistory = [];

// 🔁 Run Python script ONCE on startup to fetch predictions from MariaDB
const initPython = spawn('python', ['-u', 'main.py']);

initPython.stdout.on('data', (data) => {
    const output = data.toString().trim();
    console.log(` Python Output: ${output}`);

    try {
        // Parse only valid JSON lines as predictions
        const parsed = JSON.parse(output);
        sensorDataHistory.push({
            timestamp: new Date().toISOString(),
            predictions: parsed,
        });
    } catch (err) {
        // Ignore non-JSON lines (e.g., logs, print statements)
    }
});

initPython.stderr.on('data', (err) => {
    console.error(`Python Error: ${err}`);
});

initPython.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
});

// 📡 Serve collected predictions (Grafana / web client can query this)
app.get('/sensor-data', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.status(200).json(sensorDataHistory);
});

// 🚀 Start Node.js server
app.listen(PORT, () => {
    console.log(`Node.js server running at http://localhost:${PORT}`);
});
