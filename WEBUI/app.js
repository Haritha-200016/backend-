const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const path = require('path');

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public'))); // Serves form.html

// ✅ Connection Pool
const pool = mysql.createPool({
  host: '104.154.141.198',
  user: 'root',
  password: 'vistaarnksh',
  database: 'project',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Check if pool works
pool.getConnection((err, connection) => {
  if (err) {
    console.error('❌ DB connection failed:', err.message);
    process.exit(1); // Exit so PM2 restarts it
  }
  console.log('✅ MariaDB pool connected');
  connection.release();
});

// Endpoint: Get sector names
app.get('/sectors', (req, res) => {
  pool.query('SELECT sector_name FROM sector', (err, results) => {
    if (err) {
      console.error('❌ Error fetching sectors:', err.message);
      return res.status(500).send('Error fetching sectors');
    }
    res.json(results);
  });
});

// Submit form — insert company and device
app.post('/submit', (req, res) => {
  const {
    company_name, company_mail, sector_name, company_location,
    device_id, device_name, software_version, installation_date
  } = req.body;

  const checkCompany = 'SELECT * FROM companies WHERE company_name = ?';
  pool.query(checkCompany, [company_name], (err, companyResults) => {
    if (err) return res.send('❌ Error checking company: ' + err.sqlMessage);

    if (companyResults.length === 0) {
      const insertCompany = `
        INSERT INTO companies (company_name, company_mail, sector_name, company_location)
        VALUES (?, ?, ?, ?)`;
      pool.query(insertCompany, [company_name, company_mail, sector_name, company_location], (err2) => {
        if (err2) return res.send('❌ Error inserting company: ' + err2.sqlMessage);
        insertDeviceNow();
      });
    } else {
      const checkDevice = `
        SELECT * FROM devices WHERE company_name = ? AND device_id = ?`;
      pool.query(checkDevice, [company_name, device_id], (err3, deviceResults) => {
        if (err3) return res.send('❌ Error checking device: ' + err3.sqlMessage);

        if (deviceResults.length > 0) {
          return res.send('❌ This company is already registered with this device ID.');
        }

        insertDeviceNow();
      });
    }

    function insertDeviceNow() {
      const insertDevice = `
        INSERT INTO devices (device_id, device_name, software_version, installation_date, company_name)
        VALUES (?, ?, ?, ?, ?)`;
      pool.query(insertDevice, [device_id, device_name, software_version, installation_date, company_name], (err4) => {
        if (err4) return res.send('❌ Error inserting device: ' + err4.sqlMessage);
        res.send('✅ Company and Device registered successfully!');
      });
    }
  });
});

// Start server on port 80
app.listen(3001, '0.0.0.0', () => {
  console.log('🌐 WebUI running on http://<your-ip>/form.html');
});
s