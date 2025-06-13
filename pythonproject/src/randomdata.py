import random
import time
import schedule
from datetime import datetime
from src.dbconnection import get_mariadb_connection

def generate_mining_data():
    conn = get_mariadb_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        air_quality = random.randint(0, 500)
        co_ppm = round(random.uniform(0.0, 9.0), 2)
        co2_ppm = random.randint(200, 500)
        o2_percentage = round(random.uniform(17.0, 22.0), 2)
        humidity = random.randint(40, 90)
        water_level_m = round(random.uniform(0.0, 5.0), 2)
        seismic_activity_hz = round(random.uniform(0.1, 10.0), 2)
        noise_pollution_db = random.randint(30, 120)

        query = """
            INSERT INTO env_monitoring (
                timestamp,
                air_quality,
                co_ppm,
                co2_ppm,
                o2_percentage,
                humidity,
                water_level_m,
                seismic_activity_hz,
                noise_pollution_db
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            timestamp,
            air_quality,
            co_ppm,
            co2_ppm,
            o2_percentage,
            humidity,
            water_level_m,
            seismic_activity_hz,
            noise_pollution_db
        )

        cursor.execute(query, values)
        conn.commit()

        print(f" ENV Data inserted: Time={timestamp}, AQI={air_quality}, CO={co_ppm}, CO2={co2_ppm}, "
              f"O2={o2_percentage}, Humidity={humidity}, Water={water_level_m}, "
              f"Seismic={seismic_activity_hz}, Noise={noise_pollution_db}")

    except Exception as e:
        print(f" Error inserting env_monitoring data: {e}")
    finally:
        conn.close()


def generate_equipment_data():
    conn = get_mariadb_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        equipment_names = ["Excavator", "Crusher", "Truck", "Loader"]

        for name in equipment_names:
            temperature = round(random.uniform(70, 90), 1)
            pressure = random.randint(1300, 1600)
            motor_load = random.randint(75, 95)
            machine_runtime = random.randint(300, 700)
            fuel_consumption = random.randint(100, 150)
            tyre_pressure = random.randint(30, 45)
            battery_status = random.randint(80, 100)
            load_weight = random.randint(1000, 2000)
            latitude = round(random.uniform(18.0, 40.0), 6)
            longitude = round(random.uniform(70.0, 80.0), 6)
            gps_location = f"Latitude: {latitude}, Longitude: {longitude}"

            query = """
                INSERT INTO equipment (
                    equipment_name, temperature, pressure, gps_location,
                    motor_load, machine_runtime, fuel_consumption,
                    tyre_pressure, battery_status, load_weight,
                    timestamp, latitude, longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name, temperature, pressure, gps_location,
                motor_load, machine_runtime, fuel_consumption,
                tyre_pressure, battery_status, load_weight,
                timestamp, latitude, longitude
            )

            cursor.execute(query, values)
            print(f" EQUIP Data inserted for {name} at {timestamp}")

        conn.commit()

    except Exception as e:
        print(f" Error inserting equipment data: {e}")
    finally:
        conn.close()


# Run once immediately
generate_mining_data()
generate_equipment_data()

# Schedule every 1 minute
schedule.every(1).minutes.do(generate_mining_data)
schedule.every(1).minutes.do(generate_equipment_data)

while True:
    schedule.run_pending()
    time.sleep(60)
