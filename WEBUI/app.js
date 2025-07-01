const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const path = require('path');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public'))); // Serve form.html from /public

// MariaDB connection
const db = mysql.createConnection({
  host: '104.154.141.198',
  user: 'root',
  password: 'vistaarnksh',
  database: 'project'
});

db.connect(err => {
  if (err) {
    console.error('❌ Database connection failed:', err.message);
    process.exit(1); // Exit if DB connection fails
  }
  console.log('✅ Connected to MariaDB');
});

// API: Get all sector names
app.get('/sectors', (req, res) => {
  db.query('SELECT sector_name FROM sector', (err, results) => {
    if (err) {
      console.error('❌ Error fetching sectors:', err.message);
      return res.status(500).send('Error fetching sectors');
    }
    res.json(results);
  });
});

// API: Handle form submission
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

    // Device insertion function
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

// Start server on port 80
app.listen(3001, '0.0.0.0', () => {
  console.log('🌐 Server running on http://<your-ip>/form.html');
});
