const db = require('../dao/dao');
const mongodb = require('../dao/mongodbdao');

module.exports = {
    getcompanies: async (req, res) => {
        console.log("📥 GET /getcompanies called");

        // Check if DB object is valid
        if (!db || typeof db.query !== "function") {
            console.error("❌ DB is not connected or 'query' is not a function.");
            return res.status(500).send("Database not connected");
        }

        db.query('SELECT company_name FROM companies', (err, result) => {
            if (err) {
                console.error("❌ Error fetching company names from DB:", err);
                return res.status(500).send("Error fetching company names");
            }

            console.log("✅ Companies fetched successfully:", result);
            res.status(200).json(result);
        });
    },

    fetchall: async (req, res) => {
        try {
            const mongo = await mongodb.connectDB();
            const collection = mongo.db("landslides").collection("posts");
            const data = await collection.find({}).toArray();
            res.json(data);
        } catch (error) {
            console.error("❌ Error fetching MongoDB data:", error);
            res.status(500).send('Error fetching data');
        }
    }
};
