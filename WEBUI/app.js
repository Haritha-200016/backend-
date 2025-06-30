const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public')); // serves form.html

// Database connection
const db = mysql.createConnection({
  host: '104.154.141.198',
  user: 'root',
  password: 'vistaarnksh',
  database: 'project'
});

db.connect(err => {
  if (err) throw err;
  console.log('✅ Connected to MariaDB');
});

// Endpoint to get sector names
app.get('/sectors', (req, res) => {
  db.query('SELECT sector_name FROM sector', (err, results) => {
    if (err) return res.status(500).send('Error fetching sectors');
    res.json(results);
  });
});

// Submit form — insert company and device
app.post('/submit', (req, res) => {
  const {
    company_name, company_mail, sector_name, company_location,
    device_id, device_name, software_version, installation_date
  } = req.body;

  // Step 1: Check if company exists
  const checkCompany = 'SELECT * FROM companies WHERE company_name = ?';
  db.query(checkCompany, [company_name], (err, companyResults) => {
    if (err) return res.send('❌ Error checking company: ' + err.sqlMessage);

    if (companyResults.length === 0) {
      // Company doesn't exist — insert it
      const insertCompany = `
        INSERT INTO companies (company_name, company_mail, sector_name, company_location)
        VALUES (?, ?, ?, ?)`;
      db.query(insertCompany, [company_name, company_mail, sector_name, company_location], (err2) => {
        if (err2) return res.send('❌ Error inserting company: ' + err2.sqlMessage);
        insertDeviceNow(); // Proceed to insert device
      });
    } else {
      // Company exists — check if device ID already registered
      const checkDevice = `
        SELECT * FROM devices WHERE company_name = ? AND device_id = ?`;
      db.query(checkDevice, [company_name, device_id], (err3, deviceResults) => {
        if (err3) return res.send('❌ Error checking device: ' + err3.sqlMessage);

        if (deviceResults.length > 0) {
          return res.send('❌ This company is already registered with this device ID.');
        }

        insertDeviceNow(); // Insert device only
      });
    }

    // Function to insert device after checks
    function insertDeviceNow() {
      const insertDevice = `
        INSERT INTO devices (device_id, device_name, software_version, installation_date, company_name)
        VALUES (?, ?, ?, ?, ?)`;

      db.query(insertDevice, [device_id, device_name, software_version, installation_date, company_name], (err4) => {
        if (err4) return res.send('❌ Error inserting device: ' + err4.sqlMessage);
        res.send('✅ Company and Device registered successfully!');
      });
    }
  });
});

// Start server
//app.listen(80, () => console.log('🌐 Server running on http://localhost:3001'));
app.listen(80, '0.0.0.0', () => console.log('🌐 Server running on http://<your-ip>:80'));
