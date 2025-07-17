import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import sys
import os
import json
from datetime import datetime
from src.dbconnection import get_mariadb_connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = get_mariadb_connection()

def fetch_data_from_mariadb():
    query = 'SELECT * FROM env_monitoring ORDER BY timestamp DESC LIMIT 10'
    try:
        df = pd.read_sql(query, client)
    except Exception as e:
        print(f" Error while fetching data: {e}")
        return None

    if df.empty:
        print(" No data found in MariaDB! ")
        return None

    print(" Data fetched from MariaDB!")
    return df

# storing prediction values into MariaDB
def write_prediction_to_mariadb(data):
    client = get_mariadb_connection()
    if not client:
        print(" Could not connect to MariaDB to write data.")
        return

    cursor = client.cursor()
    query = """
        INSERT INTO predicted_data (
            timestamp,
            air_quality,
            co_ppm,
            co2_ppm,
            o2_percentage,
            humidity,
            water_level_m,
            seismic_activity_hz,
            noise_pollution_db
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["timestamp"],
        data["air_quality"],
        data["co_ppm"],
        data["co2_ppm"],
        data["o2_percentage"],
        data["humidity"],
        data["water_level_m"],
        data["seismic_activity_hz"],
        data["noise_pollution_db"]
    )

    try:
        cursor.execute(query, values)
        client.commit()
        print(" Prediction data written to MariaDB!")
    except Exception as e:
        print(f" Failed to write to MariaDB: {e}")
    finally:
        cursor.close()
        client.close()

def predict_next_value():
    df = fetch_data_from_mariadb()
    if df is None:
        print(" No data available for prediction!")
        return {}

    # Convert timestamp to numeric
    df['time_numeric'] = pd.to_datetime(df['timestamp']).astype('int64') // 10**9
    df['time_numeric'] = (df['time_numeric'] - df['time_numeric'].min()) / 60

    print(" Running predictions...")

    features = [
        "air_quality", "co_ppm", "co2_ppm", "o2_percentage",
        "humidity", "water_level_m", "seismic_activity_hz", "noise_pollution_db"
    ]

    predictions = {}

    for feature in features:
        if feature not in df.columns:
            print(f" Column '{feature}' is missing. Skipping.")
            continue

        time_steps = df[['time_numeric']]
        values = df[[feature]]

        scaler_x = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_scaled = scaler_x.fit_transform(time_steps)
        y_scaled = scaler_y.fit_transform(values)

        model = LinearRegression()
        model.fit(X_scaled, y_scaled)

        time_step_size = df['time_numeric'].diff().median()
        next_time_value = df['time_numeric'].iloc[-1] + time_step_size
        next_time = pd.DataFrame([[next_time_value]], columns=['time_numeric'])
        next_time_scaled = scaler_x.transform(next_time)

        prediction_scaled = model.predict(next_time_scaled)
        prediction = scaler_y.inverse_transform(prediction_scaled)

        predictions[feature] = round(float(prediction[0][0]), 2)

    predictions["timestamp"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    print(" Final Predictions:")
    print(json.dumps(predictions, indent=2))

    write_prediction_to_mariadb(predictions)

    return predictions

# Run prediction
predict_next_value()