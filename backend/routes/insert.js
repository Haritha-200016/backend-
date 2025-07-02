const db = require('../dao/dao');
const nodemailer = require('nodemailer');
const { MailerSend, EmailParams, Sender, Recipient } = require('mailersend');

const generateRandomNumber = () => Math.floor(1000000 + Math.random() * 9000000);

const sendMailRegistration = async (toEmail, userName) => {
  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      host: 'smtp.gmail.com',
      secure: false,
      port: 587,
      auth: {
        user: 'usha@velastra.co',
        pass: 'xzpw ixjm qpax jaim',
      },
      tls: { rejectUnauthorized: false },
    });

    const mailOptions = {
      from: 'usha@velastra.co',
      to: toEmail,
      subject: 'Welcome to Velastra!',
      text: `Hello ${userName},\n\nWelcome to Velastra! Your account has been successfully registered.\n\nBest Regards,\nVistaarnksh Team`,
    };

    let info = await transporter.sendMail(mailOptions);
    console.log(`Email sent to ${toEmail}: `, info.response);
  } catch (error) {
    console.error('Error sending welcome email:', error);
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
        user: 'usha@velastra.co',
        pass: 'xzpw ixjm qpax jaim',
      },
      tls: { rejectUnauthorized: false },
    });

    const mailOptions = {
      from: 'usha@velastra.co',
      to: companyMail,
      subject: 'New User Registration – Grant Access Required',
      text: `Hello,\n\nA new user has registered:\n
      - Name: ${userDetails.name}
      - Email: ${userDetails.email}
      - Phone: ${userDetails.phone_no}
      - Company: ${userDetails.company_name}\n\nPlease verify them.\n\nVistaarnksh Team`,
    };

    let info = await transporter.sendMail(mailOptions);
    console.log(`Email sent to ${companyMail}: `, info.response);
  } catch (error) {
    console.error('Error sending email:', error);
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

          sendMailRegistration(email, name);

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
            message: 'User registered successfully',
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
    const {
      temperature,
      humidity,
      air_quality,  // Used for both air_quality & co2_ppm
      mq7_co,       // co_ppm
      dust,
      vibration     // seismic_activity_hz
    } = req.body;

    if (
      temperature === undefined ||
      humidity === undefined ||
      air_quality === undefined ||
      mq7_co === undefined ||
      dust === undefined ||
      vibration === undefined
    ) {
      return res.status(400).json({ error: 'Missing required sensor data' });
    }

    const o2_percentage = (Math.random() * 5 + 18).toFixed(2);
    const water_level_m = (Math.random() * 5).toFixed(2);
    const noise_pollution_db = Math.floor(Math.random() * 40) + 60;

    const insertQuery = `
      INSERT INTO sensor_data (
        temperature, humidity, air_quality, co_ppm, co2_ppm,
        o2_percentage, dust, water_level_m, seismic_activity_hz, noise_pollution_db, timestamp
      )
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
    `;

    const values = [
      temperature,
      humidity,
      air_quality,
      mq7_co,
      air_quality, // reused for co2_ppm
      o2_percentage,
      dust,
      water_level_m,
      vibration,
      noise_pollution_db
    ];

    db.query(insertQuery, values, (err, result) => {
      if (err) {
        console.error('Insert error:', err);
        return res.status(500).json({ error: 'Failed to insert sensor data' });
      }

      return res.status(201).json({
        message: 'Sensor data stored successfully (with random extras)',
        id: result.insertId
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
  },

  mailersend: (req, res) => {
    const mailerSend = new MailerSend({ apiKey: process.env.API_KEY });

    const sentFrom = new Sender('usha@velastra.co', 'usha');
    const recipients = [new Recipient('ushadevarapalli43@gmail.com', 'usha')];

    const emailParams = new EmailParams()
      .setFrom(sentFrom)
      .setTo(recipients)
      .setReplyTo(sentFrom)
      .setSubject('Welcome! Your free trial is ready.')
      .setTemplateId('templateId');

    mailerSend.email
      .send(emailParams)
      .then((response) => {
        res.status(200).json({ status: 'success', message: 'Email sent', response });
      })
      .catch((error) => {
        res.status(500).json({ status: 'error', message: 'Failed to send email', error: error.message });
      });
  },
};
