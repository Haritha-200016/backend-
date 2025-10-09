import pandas as pd
import mysql.connector

# 1️⃣ Database connection
db_config = {
    "host": "104.154.141.198",
    "user": "root",
    "password": "vistaarnksh",
    "database": "project"
}

conn = mysql.connector.connect(**db_config)

# 2️⃣ Robust query to ensure numeric comparison
query = "SELECT * FROM realtime_sensor_data WHERE CAST(id AS UNSIGNED) >= 4900;"

# 3️⃣ Load into pandas DataFrame
df = pd.read_sql(query, conn)

# 4️⃣ Export to Excel
output_file = "full_data_from4900.xlsx"
df.to_excel(output_file, index=False, na_rep="NULL")

# 5️⃣ Close connection
conn.close()

print(f"✅ Data from id >= 4900 exported successfully to {output_file}")
