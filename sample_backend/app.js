const express = require('express');
const fetch = require('./routes/fetch');    // ✅ Sector & company fetching
const insert = require('./routes/insert');  // ✅ Registration & Mongo insert


const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5002;

//GET: Fetch companies by sector
app.get('/getcompanies', fetch.getcompanies);

//NEW: GET /sectors (add this line to support sector loading)
app.get('/sectors', fetch.getsectors); //This is what your Flutter needs

//POST: For testing POST body
app.post('/test', (req, res) => {
  console.log("Test API called with:", req.body);
  res.json({ message: "Test successful", received: req.body });
});

//Registration/login related
app.post('/register', insert.register);
//app.post('/registertest', insert.registertest);
app.post('/signin', insert.signin);
//app.post('/mailersend', insert.mailersend);
//app.post('/getDashboard', insert.getDashboard);
//app.post('/getDashboardDetails', insert.getDashboardDetails);
app.post('/forgot-password', insert.forgotPassword);
app.post('/api/sensor-data', insert.receiveSensorData);
app.get('/update-status', insert.updateStatus);



//Root route
app.get('/', (req, res) => {
  res.send('');
});

//Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
