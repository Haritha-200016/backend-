'''import random
import time
import schedule
from datetime import datetime
from src.dbconnection import get_mariadb_connection  # Adjust this path if needed

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
        print(f"🌱 ENV Data inserted at {timestamp}")
    except Exception as e:
        print(f"❌ Error inserting env_monitoring data: {e}")
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
            print(f"🔧 EQUIP Data inserted for {name} at {timestamp}")

        conn.commit()
    except Exception as e:
        print(f"❌ Error inserting equipment data: {e}")
    finally:
        conn.close()

def generate_worker_safety_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB for worker safety data.")
        return

    try:
        cursor = conn.cursor()

        # Define static worker IDs and random location ranges
        workers = [
            {"worker_id": 1, "latitude_range": (37.0, 38.0), "longitude_range": (-123.0, -122.0)},
            {"worker_id": 2, "latitude_range": (19.0, 20.0), "longitude_range": (72.0, 73.0)},
            {"worker_id": 3, "latitude_range": (40.0, 41.0), "longitude_range": (-75.0, -73.0)},
            {"worker_id": 4, "latitude_range": (28.0, 29.0), "longitude_range": (76.0, 78.0)},
        ]

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        for worker in workers:
            latitude = round(random.uniform(*worker["latitude_range"]), 6)
            longitude = round(random.uniform(*worker["longitude_range"]), 6)
            heart_rate = random.randint(70, 100)
            temperature = round(random.uniform(35.5, 38.0), 2)
            gas_CO = round(random.uniform(0.0, 0.05), 2)
            gas_CO2 = round(random.uniform(0.0, 0.05), 2)
            gas_NO2 = round(random.uniform(0.0, 0.05), 2)
            gas_H2S = round(random.uniform(0.0, 0.05), 2)
            man_down_alert = random.choice([0, 1])

            query = """
                INSERT INTO worker_safety (
                    worker_id, latitude, longitude, heart_rate, temperature,
                    gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert, timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    latitude = VALUES(latitude),
                    longitude = VALUES(longitude),
                    heart_rate = VALUES(heart_rate),
                    temperature = VALUES(temperature),
                    gas_CO = VALUES(gas_CO),
                    gas_CO2 = VALUES(gas_CO2),
                    gas_NO2 = VALUES(gas_NO2),
                    gas_H2S = VALUES(gas_H2S),
                    man_down_alert = VALUES(man_down_alert),
                    timestamp = VALUES(timestamp)
            """

            values = (
                worker["worker_id"], latitude, longitude, heart_rate, temperature,
                gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert, timestamp
            )

            cursor.execute(query, values)
            print(f"✅ Worker {worker['worker_id']} data updated at {timestamp}")

        conn.commit()

    except Exception as e:
        print(f"❌ Error inserting worker safety data: {e}")
    finally:
        conn.close()

# Immediate run
#generate_mining_data()
#generate_equipment_data()
#generate_worker_safety_data()

# Schedule every 1 minute
#schedule.every(1).minutes.do(generate_mining_data)
#schedule.every(1).minutes.do(generate_equipment_data)
#schedule.every(1).minutes.do(generate_worker_safety_data)

while True:
    schedule.run_pending()
    time.sleep(60)
'''







import random
import time
import schedule
from datetime import datetime
import pytz
from src.dbconnection import get_mariadb_connection  # Adjust path if needed
ist = pytz.timezone("Asia/Kolkata")


def generate_continuous_miner_data():
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return
    
    try:
        cursor = conn.cursor()
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")


        # Power & Electrical Systems
        battery_health = round(random.uniform(50.0, 100.0), 2)  # %
        voltage = round(random.uniform(200.0, 300.0), 2)        # volts
        traction_motor_temp = round(random.uniform(60.0, 120.0), 2)  # °F
        pick_wear_monitoring = round(random.uniform(0.0, 100.0), 2)  # %

        # Cutter & Drum Systems
        cutter_hours = round(random.uniform(1000.0, 2000.0), 2)      # hours
        cutter_motor_torque_kw = round(random.uniform(300.0, 500.0), 2)  # kW
        plc_control_panel_status = random.choice(["Normal", "Fault"])
        plc_fault_count = random.randint(0, 5)

        # Safety & Predictive Maintenance
        vibration_level = round(random.uniform(10.0, 100.0), 2)      # arbitrary unit

        # Hydraulic Systems
        hydraulic_pressure_psi = round(random.uniform(2500.0, 3500.0), 3)
        hydraulic_oil_level = random.choice(["Normal", "Low", "High"])
        hydraulic_oil_temp = round(random.uniform(100.0, 160.0), 2)  # °F
        hydraulic_system_status = random.choice(["Normal", "Hife", "Warning"])

        # PLC & Control Panels
        traction_control_status = random.choice(["Normal", "Fault"])
        cutter_control_status = random.choice(["Normal", "Fault"])
        plc_fault_details = random.choice([
            "No faults",
            "Overheat warning",
            "Hydraulic pressure drop",
            "Motor overload detected"
        ])

        query = """
            INSERT INTO continuous_miner (
                log_timestamp, battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            timestamp, battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
            cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
            vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
            hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details
        )

        cursor.execute(query, values)
        conn.commit()
        print(f"🛠 Continuous Miner data inserted at {timestamp}")

    except Exception as e:
        print(f"❌ Error inserting continuous miner data: {e}")
    finally:
        conn.close()

# Schedule to run every 3 minutes
schedule.every(3).minutes.do(generate_continuous_miner_data)

# Immediate first run
generate_continuous_miner_data()

while True:
    schedule.run_pending()
    time.sleep(1)
