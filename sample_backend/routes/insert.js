const db = require('../dao/dao');
const nodemailer = require('nodemailer');
const { MailerSend, EmailParams, Sender, Recipient } = require('mailersend');

const generateRandomNumber = () => Math.floor(1000000 + Math.random() * 9000000);

const sendStatusMailToUser = async (toEmail, userName, status) => {
  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      host: 'smtp.gmail.com',
      secure: false,
      port: 587,
      auth: {
        user: 'haritha@velastra.co',
        pass: 'zbch zaom fcxs kmlf',
      },
      tls: { rejectUnauthorized: false },
    });

    const mailOptions = {
      from: 'haritha@velastra.co',
      to: toEmail,
      subject: `Your Registration Status: ${status.toUpperCase()}`,
      text: `Hello ${userName},\n\nYour registration status is now: ${status.toUpperCase()}.\n\nThank you,\nVistaarnksh Team`,
    };

    const info = await transporter.sendMail(mailOptions);
    console.log(`✅ Status mail sent to ${toEmail}:`, info.response);
  } catch (error) {
    console.error('❌ Error sending status mail to user:', error);
  }
};



const sendMailToCompany = async (companyMail, userDetails) => {
  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      host: 'smtp.gmail.com',
      secure: false,
      port: 587,
      auth: {
        user: 'haritha@velastra.co',
        pass: 'zbch zaom fcxs kmlf',
      },
      tls: { rejectUnauthorized: false },
    });

    const mailOptions = {
      from: 'haritha@velastra.co',
      to: companyMail,
      subject: 'New User Registration – Grant Access Required',
      html: `
        <p>Hello,</p>
        <p>A new user has registered:</p>
        <ul>
          <li><b>Name:</b> ${userDetails.name}</li>
          <li><b>Email:</b> ${userDetails.email}</li>
          <li><b>Phone:</b> ${userDetails.phone_no}</li>
          <li><b>Company:</b> ${userDetails.company_name}</li>
        </ul>
        <p>Please take an action:</p>
        <a href="http://104.154.141.198:5002/update-status?phone_no=${userDetails.phone_no}&status=verified"
           style="padding:10px 20px;background-color:#4CAF50;color:white;text-decoration:none;border-radius:4px;">✅ Approve</a>
        &nbsp;
        <a href="http://104.154.141.198:5002/update-status?phone_no=${userDetails.phone_no}&status=rejected"
           style="padding:10px 20px;background-color:#f44336;color:white;text-decoration:none;border-radius:4px;">❌ Reject</a>
        &nbsp;
        <a href="http://104.154.141.198:5002/update-status?phone_no=${userDetails.phone_no}&status=in%20progress"
           style="padding:10px 20px;background-color:#ff9800;color:white;text-decoration:none;border-radius:4px;">⏳ In Progress</a>
        <br><br>
        <p>— Vistaarnksh Team</p>
      `,
    };

    const info = await transporter.sendMail(mailOptions);
    console.log(`✅ Email successfully sent to ${companyMail}:`, info.response);
  } catch (error) {
    console.error('❌ Failed to send email to company:', {
      message: error.message,
      stack: error.stack,
    });
  }
};


module.exports = {
  register: (req, res) => {
    const { name, phone_no, email, password, sector_name, company_name } = req.body;
    const randomNumber = generateRandomNumber();
    const access = 'in progress';

    if (!name || !email || !password || !phone_no || !sector_name || !company_name) {
      return res.status(400).json({ message: 'All fields are required including sector' });
    }

    const checkQuery = `SELECT * FROM users WHERE phone_no = ? OR email = ?`;
    db.query(checkQuery, [phone_no, email], (err, existingUsers) => {
      if (err) {
        console.error('Error checking existing user:', err);
        return res.status(500).json({ message: 'Database error during duplicate check' });
      }

      if (existingUsers.length > 0) {
        return res.status(409).json({
          message: 'User already registered with this phone number or email',
        });
      }

      const insertQuery = `
        INSERT INTO users (user_id, name, phone_no, email, password, access, sector_name, company_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `;

      db.query(
        insertQuery,
        [randomNumber, name, phone_no, email, password, access, sector_name, company_name],
        (err, result) => {
          if (err) {
            console.error('Error inserting user:', err);
            return res.status(500).json({ message: 'Database error during insert' });
          }

          sendStatusMailToUser(email, name, 'in progress');


          const query1 = `SELECT company_mail FROM companies WHERE sector_name = ? AND company_name = ?`;
          db.query(query1, [sector_name, company_name], (err, results) => {
            if (err) {
              console.error('Error fetching company mail:', err);
              return;
            }

            if (results.length > 0) {
              const companyMail = results[0].company_mail;
              sendMailToCompany(companyMail, { name, email, phone_no, sector_name, company_name });
            }
          });

          return res.status(201).json({
            status: 'success',
            message: 'Registration successful! Approval may take up to 24 hours',
            user_id: randomNumber,
            name,
            email,
            sector_name,
            company_name,
          });
        }
      );
    });
  },

  signin: (req, res) => {
  const { phone_no, password } = req.body;

  if (!phone_no || !password)
    return res.status(400).json({ message: 'Please provide valid credentials.' });

  const query = 'SELECT * FROM users WHERE phone_no = ? AND password = ?';
  db.query(query, [phone_no, password], (err, result) => {
    if (err) return res.status(500).json({ message: 'Database error' });

    if (result.length > 0) {
      const user = result[0];

      if (user.access !== 'verified') {
        return res.status(403).json({
          status: 'pending',
          message: 'Access not verified yet. Please wait for company approval.',
        });
      }

      return res.status(200).json({
        status: 'success',
        message: 'Login successful',
        user: {
          user_id: user.user_id,
          name: user.name,
          phone_no: user.phone_no,
          email: user.email,
          sector_name: user.sector_name,
          company_name: user.company_name,
          access: user.access,
        },
      });
    } else {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
  });
},

  forgotPassword: (req, res) => {
    const { phone_no, password } = req.body;
    if (!phone_no || !password)
      return res.status(400).json({ message: 'Phone number and password required' });

    const cleanPhone = phone_no.trim();

    const checkQuery = `SELECT * FROM users WHERE phone_no = ?`;
    db.query(checkQuery, [cleanPhone], (err, result) => {
      if (err) return res.status(500).json({ message: 'Database error' });

      if (result.length === 0)
        return res.status(404).json({ message: 'User not found' });

      const updateQuery = `UPDATE users SET password = ? WHERE phone_no = ?`;
      db.query(updateQuery, [password, cleanPhone], (err, updateResult) => {
        if (err) return res.status(500).json({ message: 'Error updating password' });

        return res.status(200).json({ message: 'Password updated successfully' });
      });
    });
  },

  receiveSensorData: (req, res) => {
    const { temperature, humidity, air_quality, mq7_co, dust } = req.body;

    if (
      temperature === undefined ||
      humidity === undefined ||
      air_quality === undefined ||
      mq7_co === undefined ||
      dust === undefined
    ) {
      return res.status(400).json({ error: 'Missing sensor data' });
    }

    const insertQuery = `
      INSERT INTO sensot_data (temperature, humidity, co2_ppm, co_ppm, dust, timestamp)
      VALUES (?, ?, ?, ?, ?, NOW())
    `;

    db.query(insertQuery, [temperature, humidity, air_quality, mq7_co, dust], (err, result) => {
      if (err) return res.status(500).json({ error: 'SQL insert failed' });

      return res.status(201).json({
        message: 'Sensor data stored successfully',
        id: result.insertId,
      });
    });
  },

updateStatus: (req, res) => {
  const { phone_no, status } = req.query;

  if (!phone_no || !status) {
    return res.status(400).send('Missing phone_no or status');
  }

  const updateQuery = `UPDATE users SET access = ? WHERE phone_no = ?`;
  db.query(updateQuery, [status, phone_no], (err, result) => {
    if (err) {
      console.error('❌ Database update error:', err);
      return res.status(500).send('Database error');
    }

    const fetchQuery = `SELECT email, name FROM users WHERE phone_no = ?`;
    db.query(fetchQuery, [phone_no], async (err, rows) => {
      if (err || rows.length === 0) {
        console.error('❌ Error fetching user:', err);
        return res.status(404).send('User not found');
      }

      const { email, name } = rows[0];
      await sendStatusMailToUser(email, name, status);

      return res.send(`✅ Status updated to "${status}" and mail sent to ${email}`);
    });
  });
},

  getDashboard: (req, res) => {
    const { company_name } = req.body;
    if (!company_name) return res.status(400).json({ message: 'Company name is required' });

    const getCompanyIdQuery = `SELECT company_id FROM companies WHERE company_name = ?`;

    db.query(getCompanyIdQuery, [company_name], (err, companyResult) => {
      if (err) return res.status(500).json({ error: 'Database error' });
      if (companyResult.length === 0)
        return res.status(404).json({ message: 'Company not found' });

      const companyId = companyResult[0].company_id;

      const getDashboardQuery = `
        SELECT * FROM dashboards d
        LEFT JOIN dashboard_data dd ON d.dashboard_id = dd.dashboard_id
        WHERE d.company_id = ?
      `;

      db.query(getDashboardQuery, [companyId], (err, result) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        if (result.length > 0) {
          return res.status(200).json({ status: 'success', data: result });
        } else {
          return res.status(404).json({ message: 'No dashboard data found' });
        }
      });
    });
  },

  getDashboardDetails: (req, res) => {
    const { user_id } = req.body;
    if (!user_id) return res.status(400).json({ message: 'User ID is required' });

    const query = `
      SELECT dd.*, d.*
      FROM users u
      JOIN companies c ON u.company_name = c.company_name
      JOIN dashboards d ON c.company_id = d.company_id
      JOIN dashboard_data dd ON d.dashboard_id = dd.dashboard_id
      WHERE u.user_id = ? AND u.access = 'verified'
    `;

    db.query(query, [user_id], (err, result) => {
      if (err) return res.status(500).json({ error: 'Database error' });

      if (result.length > 0) {
        return res.status(200).json({ status: 'success', data: result });
      } else {
        return res.status(404).json({ message: 'No dashboard data found' });
      }
    });
  }
}