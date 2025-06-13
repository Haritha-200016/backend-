
const db = require('../dao/dao');
const mongodb = require('../dao/mongodbdao')


module.exports  = {
    

    getcompanies: async (req, res) => {
        db.query('SELECT company_name FROM companies', (err, result) => {
            if (err) {
                console.log("Error fetching company names:", err);
                res.status(500).send("Error getting company names, please try to refresh.");
            } else {
                res.send(result); 
            }
        });
    },

    fetchall: async (req, res) => {
        try {
            const mongo = await mongodb.connectDB();
            const collection = mongo.db("landslides").collection("posts");  
            const data = await collection.find({}).toArray();  
            res.json(data);  
        } catch (error) {
            console.error("Error fetching data:", error);
            res.status(500).send('Error fetching data');
        }
    },

    
}
 




