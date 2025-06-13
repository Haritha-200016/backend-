
const db = require('../dao/dao');
const mongodb = require('../dao/mongodbdao')
const nodemailer =require('nodemailer');
const { MailerSend, EmailParams, Sender, Recipient } = require('mailersend');

const generateRandomNumber = () => {
    return Math.floor(1000000 + Math.random() * 9000000); 
  }

const sendMailRegistration = async (toEmail, userName) => {
    try {
        let transporter = nodemailer.createTransport({
            service: 'gmail',
            host: "smtp.gmail.com",
            secure: false,
            port: 587,
            auth: {
                user: 'naveenyadav1128@gmail.com',
                pass: 'enfh vupd pjbm ozkj' 
            }
        });

        let mailOptions = {
            from: "naveenyadav1128@gmail.com",
            to: toEmail, 
            subject: "Welcome to Vistaarnksh!",
            text: `Hello ${userName},\n\nWelcome to Vistaarnksh! Your account has been successfully registered.\n\nBest Regards,\nVistaarnksh Team`
        };

        let info = await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${toEmail}: `, info.response);
    } catch (error) {
        console.error("Error sending welcome email:", error);
    }
};

const sendMailToCompany = async (companyMail , userDetails) => { 
    try {
        let transporter = nodemailer.createTransport({
            service: 'gmail',
            host: "smtp.gmail.com",
            secure: false,
            port: 587,
            auth: {
                user: 'naveenyadav1128@gmail.com',
                pass: 'enfh vupd pjbm ozkj'
            }
        });

        let mailOptions = {
            from: "naveenyadav1128@gmail.com",
            to: companyMail, 
            subject: "New User Registration – Grant Access Required",
            text: `Hello,\n\nA new user has registered for your company. Below are the details:\n
            - Name: ${userDetails.name}
            - Email: ${userDetails.email}
            - Phone: ${userDetails.phone_no}
            - Company: ${userDetails.company_name}

            Please review their details and grant access if necessary.\n\nBest Regards,\nVistaarnksh Team`
        };

        let info = await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${companyMail}: `, info.response);
    } catch (error) {
        console.error("Error sending email:", error);
    }
};



module.exports  = {

    getDashboardDetails: (req, res) => {
        const { user_id } = req.body; // Ensure 'user_id' is used
    
        if ( !user_id) {  // Use the correct variable names
            return res.status(400).json({ message: "Company name and user ID are required" });
        }
    
            const getDashboarddata = `SELECT 
                dd.*,
                d.*
            FROM 
                users u
            JOIN 
                companies c ON u.company_name = c.company_name
            JOIN 
                dashboards d ON c.company_id = d.company_id
            JOIN 
                dashboard_data dd ON d.dashboard_id = dd.dashboard_id
            WHERE 
                u.user_id = ?
                AND u.access = 'verified'`;
    
            db.query(getDashboarddata, [user_id], (err, result) => {
                if (err) {
                    console.error('Error fetching dashboard data:', err);
                    return res.status(500).json({ error: 'Database error' });
                }
    
                if (result.length > 0) {
                    return res.status(200).json({
                        status: 'success',
                        data: result
                    });
                } else {
                    return res.status(404).json({ message: 'No dashboard data found for this company' });
                }
            });
    },
     

    getDashboard : (req, res) => {
        const { company_name } = req.body;
        console.log("called getDashboard");
    
        if (!company_name) {
            return res.status(400).json({ message: 'Company name is required' });
        }
    
        const getCompanyIdQuery = `
            SELECT company_id FROM companies 
            WHERE company_name = ?
        `;
    
        db.query(getCompanyIdQuery, [company_name], (err, companyResult) => {
            if (err) {
                console.error('Error fetching company ID:', err);
                return res.status(500).json({ error: 'Database error' });
            }
    
            if (companyResult.length === 0) {
                return res.status(404).json({ message: 'Company not found' });
            }
    
            const companyId = companyResult[0].company_id;
    
            const getDashboardQuery = `
                SELECT 
                    *
                FROM 
                    dashboards d
                LEFT JOIN 
                    dashboard_data dd ON d.dashboard_id = dd.dashboard_id
                WHERE 
                    d.company_id = ?
            `;
    
            db.query(getDashboardQuery, [companyId], (err, result) => {
                if (err) {
                    console.error('Error fetching dashboard data:', err);
                    return res.status(500).json({ error: 'Database error' });
                }
    
                if (result.length > 0) {
                    return res.status(200).json({
                        status: 'success',
                        data: result
                    });
                } else {
                    return res.status(404).json({ message: 'No dashboard data found for this company' });
                }
            });
        });
    },
    
    mailersend: (req, res) => {
            console.log('Mailersend route hit'); 
            const mailerSend = new MailerSend({
                apiKey: process.env.API_KEY,
            });
        
            const sentFrom = new Sender("naveenyadav1128@gmail.com", "Naveen");
        
            const recipients = [
                new Recipient("ushadevarapalli43@gmail.com", "usha")
            ];
        
            const emailParams = new EmailParams()
                .setFrom(sentFrom)
                .setTo(recipients)
                .setReplyTo(sentFrom)
                .setSubject("Welcome! Your free trial is ready.")
                .setTemplateId('templateId');
        
            mailerSend.email.send(emailParams)
                .then(response => {
                    console.log("Email sent successfully:", response);
                    res.status(200).json({
                        status: 'success',
                        message: 'Email sent successfully',
                        response
                    });
                })
                .catch(error => {
                    console.error("Error sending email:", error);
                    res.status(500).json({
                        status: 'error',
                        message: 'Failed to send email',
                        error: error.message
                    });
                });
        },

   

    register : (req, res) => {
        const { name, phone_no, email, password, company_name } = req.body;
        console.log(req.body);
        const randomNumber = generateRandomNumber();
        const access = "in progress";
    
        if (!name || !email || !password || !phone_no || !company_name) {
            return res.status(400).json({ error: 'Name, email, phone number, and password are required' });
        }
    
        const query = `
            INSERT INTO users (user_id, name, phone_no, email, password, access, company_name) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        `;
    
        db.query(query, [randomNumber, name, phone_no, email, password, access, company_name], (err, result) => {
            if (err) {
                console.error('Error inserting user:', err);
                return res.status(500).json({ error: 'Database error' });
            } else {
                sendMailRegistration(email, name);
    
                // ✅ Fetch company email only if user insertion is successful
                const query1 = `SELECT company_mail FROM companies WHERE company_name = ?`;
    
                db.query(query1, [company_name], (err, results) => {
                    if (err) {
                        console.error("Error fetching company mail:", err);
                        return res.status(500).json({ error: "Database error while fetching company email" });
                    }
    
                    if (results.length > 0) {
                        const companyMail = results[0].company_mail;
                        sendMailToCompany(companyMail , { name, email, phone_no, company_name } );
                    }
                });
    
                return res.status(201).json({
                    status: 'success',
                    message: 'User registered successfully',
                    user_id: randomNumber,
                    name: name,
                    email: email,
                    company_name: company_name
                });
            }
        });
    },

    signin: (req, res) => {
        const { phone_no, password } = req.body;
        console.log(req.body);
        console.log("Api is called successfully");
    
        if (!phone_no || !password) {
            return res.status(400).json({
                message: "Please provide a valid phone number and password or register if you haven't."
            });
        }
    
        const query = `SELECT * FROM users WHERE phone_no = ? AND password = ?`;
    
        db.query(query, [phone_no, password], (err, result) => {
            if (err) {
                console.error('Error logging in:', err);
                return res.status(500).json({ error: 'Database error' });
            }
    
            if (result.length > 0) {
                
                console.log("data status success");

                const user = result[0];
                return res.status(200).json({
                    status: 'success',
                    message: 'Login successful',
                    user: {
                        user_id: user.user_id,
                        name: user.name,
                        phone_no: user.phone_no,
                        email: user.email,
                        company_name: user.company_name,
                        access: user.access
                    }
                });
            } else {
                console.log("error while sending");
                return res.status(401).json({ error: 'Invalid phone number or password' });
            }
        });
    },
    

    registertest :  (req ,res ) =>{
        const postdata = req.body;
        console.log(postdata);
        const {name , phone_no ,email ,password ,company_name} = req.body;
        const randomNumber = generateRandomNumber();
        //const company_id = 1931885
        const access = "in progress"

        if (!name || !email || !password || !phone_no || !company_name)  {
            return res.status(400).json({ error: 'Name, email, and password are required' });
        }
        
        const query = `
        INSERT INTO users (user_id, name, phone_no, email, password,access,company_name) 
        VALUES (?, ?, ?, ?, ?,? ,?)`;

        db.query(query, [randomNumber, name, phone_no, email, password , access,company_name] , (err,result) =>{
            if (err) {
                console.error('Error inserting user:', err);
                return res.status(500).json({ error: 'Database error' });
            }else{
                sendMail(email, name);
                return res.status(201).json({
                    status: 'success',
                    message: 'User registered successfully',
                    user_id: randomNumber,
                    name: name,
                    email: email,
                    company_name: company_name
                });
            }
        } )
    },

    insertDht: async (req, res) => {
        try {
            const postData = req.body; // Get data from the request body
            const dbcon = await mongodb.connectDB() // Ensure DB is connected
            const collection = dbcon.db("landslides").collection("posts"); // Access the 'posts' collection
            const result = await collection.insertOne(postData); // Insert data into the collection
            console.log(postData);
            res.status(200).json({
                message: 'Data inserted successfully',
                insertedId: result.insertedId // Return the inserted document's ID
            });
        } catch (e) {
            console.error("Error inserting data:", e); // Log the error
            res.status(500).json({
                error: 'An error occurred while inserting data',
                details: e.message // Return the error message to the client
            });
        }
    },
    

    
}
 
