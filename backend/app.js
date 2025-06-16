const express = require('express');
const fetch = require('./routes/fetch');
const insert = require('./routes/insert')

const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5001;



app.get('/getcompanies',fetch.getcompanies);
app.post('/test', (req, res) => {
    console.log("Test API called with:", req.body);
    res.json({ message: "Test successful", received: req.body });
});

app.post('/register',insert.register);
app.post('/registertest',insert.registertest);
app.post('/signin', insert.signin);
app.post('/mailersend',insert.mailersend);
app.post('/getDashboard',insert.getDashboard);
app.post('/getDashboardDetails',insert.getDashboardDetails);


app.get('/fetchall', fetch.fetchall)   // nosql
app.post('/postdata', insert.insertDht) // nosql

// Root Route
app.get('/', (req, res) => {
    res.send('');
});

// Start the Express Server on Port 5000
app.listen(PORT,'0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});


