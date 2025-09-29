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








import random
import time
import schedule
from datetime import datetime, timedelta
import pytz
from src.dbconnection import get_mariadb_connection

ist = pytz.timezone("Asia/Kolkata")

def generate_all_sensor_data():
    devices = ["d1", "d2", "d4", "d5"]
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return

    try:
        cursor = conn.cursor()
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

        for Device_id in devices:
            for motor in ["M1", "M2", "M3", "M4"]:

            # 🌍 Environmental Monitoring
                air_quality = random.randint(0, 500)
                co_ppm = round(random.uniform(0.0, 9.0), 2)
                co2_ppm = random.randint(200, 500)
                o2_percentage = round(random.uniform(17.0, 22.0), 2)
                humidity = random.randint(40, 90)
                water_level_m = round(random.uniform(0.0, 5.0), 2)
                seismic_activity_hz = round(random.uniform(0.1, 10.0), 2)
                noise_pollution_db = random.randint(30, 120)

                # ⚙️ Equipment Data
                equipment_name = random.choice(["Excavator", "Crusher", "Truck", "Loader"])
                temperature = round(random.uniform(70, 90), 1)
                pressure = round(random.randint(1300, 1600))
                motor_load = random.randint(75, 95)
                machine_runtime = random.randint(300, 700)
                fuel_consumption = random.randint(100, 150)
                tyre_pressure = random.randint(30, 45)
                battery_status = random.randint(80, 100)
                load_weight = random.randint(1000, 2000)
                latitude = round(random.uniform(18.0, 40.0), 6)
                longitude = round(random.uniform(70.0, 80.0), 6)

                # 🦺 Worker Safety
                worker_id = f"W{random.randint(1, 10)}"
                heart_rate = random.randint(70, 100)
                gas_CO = round(random.uniform(0.0, 0.05), 2)
                gas_CO2 = round(random.uniform(0.0, 0.05), 2)
                gas_NO2 = round(random.uniform(0.0, 0.05), 2)
                gas_H2S = round(random.uniform(0.0, 0.05), 2)
                man_down_alert = random.choice([0, 1])

                # ⛏️ Continuous Miner & RAM Car
                battery_health = round(random.uniform(50.0, 100.0), 2)
                voltage = round(random.uniform(200.0, 300.0), 2)
                traction_motor_temp = round(random.uniform(60.0, 120.0), 2)
                pick_wear_monitoring = round(random.uniform(0.0, 100.0), 2)
                cutter_hours = round(random.uniform(1000.0, 2000.0), 2)
                cutter_motor_torque_kw = round(random.uniform(300.0, 500.0), 2)
                plc_control_panel_status = random.choice(["Normal", "Fault"])
                plc_fault_count = random.randint(0, 5)
                vibration_level = round(random.uniform(10.0, 100.0), 2)
                hydraulic_pressure_psi = round(random.uniform(2500.0, 3500.0), 2)
                hydraulic_oil_level = round(random.uniform(30, 100), 2)  # float
                hydraulic_oil_temp = round(random.uniform(100.0, 160.0), 2)
                hydraulic_system_status = random.choice(["Normal", "High", "Warning"])
                traction_control_status = random.choice(["Normal", "Fault"])
                cutter_control_status = random.choice(["Normal", "Fault"])
                plc_fault_details = random.choice([
                    "No faults", "Overheat warning", "Hydraulic pressure drop", "Motor overload detected"
                ])
                #Ram Car
                exhaust_gas_ppm = round(random.uniform(200.0, 500.0), 2)
                engine_heat = round(random.uniform(70.0, 120.0), 2)
                oil_pressure_bar = round(random.uniform(1.0, 6.0), 3)
                coolant_temperature = round(random.uniform(60.0, 100.0), 2)
                oil_pressure = round(random.uniform(20.0, 80.0), 2)
                total_hours = random.randint(500, 3000)
                reining = round(random.uniform(0.0, 100.0), 2)
                #motor = random.choice(["M1", "M2", "M3", "M4"])
                date_of_fitment = (datetime.now() - timedelta(days=random.randint(100, 1000))).date()
                remaining_hours = random.randint(50, 1000)

                # Mining Metrics
                active_blast_areas = round(random.uniform(0, 5), 2)
                development_meters = round(random.uniform(0, 500), 2)
                production_meters = round(random.uniform(0, 1000), 2)
                ore_mined = round(random.uniform(0, 10000), 2)
                throughput = round(random.uniform(50, 500), 2)
                crusher_availability = round(random.uniform(70, 100), 2)
                mill_vibration = round(random.uniform(0, 10), 2)
                dump_trucks_utilization = round(random.uniform(50, 100), 2)
                excavators_utilization = round(random.uniform(50, 100), 2)
                drills_utilization = round(random.uniform(50, 100), 2)
                dust = round(random.uniform(0, 500), 2)

            # 🔽 Insert into dummy
            query = """
                INSERT INTO dummy (
                    id,device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                    water_level_m, seismic_activity_hz, noise_pollution_db, equipment_name,
                    temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                    tyre_pressure, battery_status, load_weight, latitude, longitude,
                    worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                    battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                    cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                    vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                    hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                    exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                    total_hours, reining, motor, date_of_fitment, remaining_hours,
                    active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                    crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                    drills_utilization, dust
                ) VALUES (
                    NULL, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                )
            """

            values = (
                Device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                water_level_m, seismic_activity_hz, noise_pollution_db, equipment_name,
                temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                tyre_pressure, battery_status, load_weight, latitude, longitude,
                worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                total_hours, reining, motor, date_of_fitment, remaining_hours,
                active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                drills_utilization, dust
            )

            cursor.execute(query, values)

        conn.commit()
        print(f"✅ All sensor data inserted at {timestamp}")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()


# Schedule every 2 minutes
schedule.every(2).minutes.do(generate_all_sensor_data)

# Run immediately
generate_all_sensor_data()

while True:
    schedule.run_pending()
    time.sleep(1)




import random
import time
import schedule
from datetime import datetime, timedelta
import pytz
from src.dbconnection import get_mariadb_connection

# Indian timezone
ist = pytz.timezone("Asia/Kolkata")

# Helper → Generate random GPS around base location
def random_gps(base_lat=23.456, base_lng=85.123):
    return (
        round(base_lat + (random.random() - 0.5) * 0.01, 6),
        round(base_lng + (random.random() - 0.5) * 0.01, 6)
    )

def generate_all_sensor_data():
    devices = ["d1", "d2", "d3", "d4", "d5"]
    conn = get_mariadb_connection()
    if not conn:
        print("❌ Failed to connect to MariaDB.")
        return

    try:
        cursor = conn.cursor()
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

        for device_id in devices:
            # 🌍 Environmental Monitoring
            air_quality = random.randint(0, 500)
            co_ppm = round(random.uniform(0.0, 9.0), 2)
            co2_ppm = random.randint(200, 500)
            o2_percentage = round(random.uniform(17.0, 22.0), 2)
            humidity = random.randint(40, 90)
            water_level_m = round(random.uniform(0.0, 5.0), 2)
            seismic_activity_hz = round(random.uniform(0.1, 10.0), 2)
            noise_pollution_db = random.randint(30, 120)

            # ⚙️ Equipment Data
            temperature = round(random.uniform(70, 90), 1)
            pressure = round(random.randint(1300, 1600))
            motor_load = random.randint(75, 95)
            machine_runtime = random.randint(300, 700)
            fuel_consumption = random.randint(100, 150)
            tyre_pressure = random.randint(30, 45)
            battery_status = random.randint(80, 100)
            load_weight = random.randint(1000, 2000)

            # 🦺 Worker Safety
            worker_id = f"W{random.randint(1, 10)}"
            heart_rate = random.randint(70, 100)
            gas_CO = round(random.uniform(0.0, 0.05), 2)
            gas_CO2 = round(random.uniform(0.0, 0.05), 2)
            gas_NO2 = round(random.uniform(0.0, 0.05), 2)
            gas_H2S = round(random.uniform(0.0, 0.05), 2)
            man_down_alert = random.choice([0, 1])

            # ⛏️ Continuous Miner & RAM Car
            battery_health = round(random.uniform(50.0, 100.0), 2)
            voltage = round(random.uniform(200.0, 300.0), 2)
            traction_motor_temp = round(random.uniform(60.0, 120.0), 2)
            pick_wear_monitoring = round(random.uniform(0.0, 100.0), 2)
            cutter_hours = round(random.uniform(1000.0, 2000.0), 2)
            cutter_motor_torque_kw = round(random.uniform(300.0, 500.0), 2)
            plc_control_panel_status = random.choice(["Normal", "Fault"])
            plc_fault_count = random.randint(0, 5)
            vibration_level = round(random.uniform(10.0, 100.0), 2)
            hydraulic_pressure_psi = round(random.uniform(2500.0, 3500.0), 2)
            hydraulic_oil_level = round(random.uniform(30, 100), 2)
            hydraulic_oil_temp = round(random.uniform(100.0, 160.0), 2)
            hydraulic_system_status = random.choice(["Normal", "High", "Warning"])
            traction_control_status = random.choice(["Normal", "Fault"])
            cutter_control_status = random.choice(["Normal", "Fault"])
            plc_fault_details = random.choice([
                "No faults", "Overheat warning", "Hydraulic pressure drop", "Motor overload detected"
            ])

            # Ram Car
            exhaust_gas_ppm = round(random.uniform(200.0, 500.0), 2)
            engine_heat = round(random.uniform(70.0, 120.0), 2)
            oil_pressure_bar = round(random.uniform(1.0, 6.0), 3)
            coolant_temperature = round(random.uniform(60.0, 100.0), 2)
            oil_pressure = round(random.uniform(20.0, 80.0), 2)
            total_hours = random.randint(500, 3000)
            reining = round(random.uniform(0.0, 100.0), 2)
            motor = random.choice(["Motor_A", "Motor_B", "Motor_C"])  # Added motor value
            date_of_fitment = (datetime.now() - timedelta(days=random.randint(100, 1000))).date()
            remaining_hours = random.randint(50, 1000)

            # Mining Metrics
            active_blast_areas = round(random.uniform(0, 5), 2)
            development_meters = round(random.uniform(0, 500), 2)
            production_meters = round(random.uniform(0, 1000), 2)
            ore_mined = round(random.uniform(0, 10000), 2)
            throughput = round(random.uniform(50, 500), 2)
            crusher_availability = round(random.uniform(70, 100), 2)
            mill_vibration = round(random.uniform(0, 10), 2)
            dump_trucks_utilization = round(random.uniform(50, 100), 2)
            excavators_utilization = round(random.uniform(50, 100), 2)
            drills_utilization = round(random.uniform(50, 100), 2)
            dust = round(random.uniform(0, 500), 2)

            # Common insert query with all 66 columns
            query = """
                INSERT INTO dummy (
                    device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                    water_level_m, seismic_activity_hz, noise_pollution_db, equipment_name,
                    temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                    tyre_pressure, battery_status, load_weight, latitude, longitude,
                    worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                    battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                    cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                    vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                    hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                    exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                    total_hours, reining, motor, date_of_fitment, remaining_hours,
                    active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                    crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                    drills_utilization, dust
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            if device_id == "d3":
                # One Excavator
                latitude, longitude = random_gps()
                cursor.execute(query, (
                    device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                    water_level_m, seismic_activity_hz, noise_pollution_db, "Excavator",
                    temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                    tyre_pressure, battery_status, load_weight, latitude, longitude,
                    worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                    battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                    cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                    vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                    hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                    exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                    total_hours, reining, motor, date_of_fitment, remaining_hours,
                    active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                    crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                    drills_utilization, dust
                ))

                # Five Haulers
                for i in range(5):
                    latitude, longitude = random_gps()
                    cursor.execute(query, (
                        device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                        water_level_m, seismic_activity_hz, noise_pollution_db, f"Hauler-{i+1}",
                        temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                        tyre_pressure, battery_status, load_weight, latitude, longitude,
                        worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                        battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                        cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                        vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                        hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                        exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                        total_hours, reining, motor, date_of_fitment, remaining_hours,
                        active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                        crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                        drills_utilization, dust
                    ))
            else:
                # Other devices (Generic, no GPS)
                latitude, longitude = None, None
                cursor.execute(query, (
                    device_id, timestamp, air_quality, co_ppm, co2_ppm, o2_percentage, humidity,
                    water_level_m, seismic_activity_hz, noise_pollution_db, "Generic",
                    temperature, pressure, motor_load, machine_runtime, fuel_consumption,
                    tyre_pressure, battery_status, load_weight, latitude, longitude,
                    worker_id, heart_rate, gas_CO, gas_CO2, gas_NO2, gas_H2S, man_down_alert,
                    battery_health, voltage, traction_motor_temp, pick_wear_monitoring,
                    cutter_hours, cutter_motor_torque_kw, plc_control_panel_status, plc_fault_count,
                    vibration_level, hydraulic_pressure_psi, hydraulic_oil_level, hydraulic_oil_temp,
                    hydraulic_system_status, traction_control_status, cutter_control_status, plc_fault_details,
                    exhaust_gas_ppm, engine_heat, oil_pressure_bar, coolant_temperature, oil_pressure,
                    total_hours, reining, motor, date_of_fitment, remaining_hours,
                    active_blast_areas, development_meters, production_meters, ore_mined, throughput,
                    crusher_availability, mill_vibration, dump_trucks_utilization, excavators_utilization,
                    drills_utilization, dust
                ))

        conn.commit()
        print(f"✅ Sensor data inserted at {timestamp}")

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    finally:
        conn.close()

# Schedule every 2 minutes
schedule.every(1).minutes.do(generate_all_sensor_data)

# Run once immediately
generate_all_sensor_data()

while True:
    schedule.run_pending()
    time.sleep(1)


'''








import time
import itertools
from src.dbconnection import get_mariadb_connection
import pandas as pd
from datetime import datetime, timezone, timedelta

# 1️⃣ Read Excel file
file_path = r"src\realtime.xlsx"
df = pd.read_excel(file_path)

# 2️⃣ Database connection
db = get_mariadb_connection()
cursor = db.cursor()

# 3️⃣ Correct table name
table = "realtime_sensor_data"

# 4️⃣ Clean DataFrame and exclude 'id' from insertion
df = df.where(pd.notnull(df), None)   # Replace NaN → None
# Remove 'id' from the records since it's auto-incremented
records = [{k: v for k, v in row.items() if k != 'id'} for row in df.to_dict(orient="records")]

def convert_value(value):
    """Convert numpy types to native Python types"""
    if value is None:
        return None
    if hasattr(value, "item"):  # numpy.int64, numpy.float64
        return value.item()
    return value

# 5️⃣ Insert rows in continuous loop
for row in itertools.cycle(records):
    try:
        # Add current timestamp in IST
        ist = timezone(timedelta(minutes=330))
        current_timestamp = datetime.now(ist).strftime('%Y-%m-%dT%H:%M:%SZ')
        row['timestamp'] = current_timestamp
        
        values = [convert_value(v) for v in row.values()]
        placeholders = ", ".join(["%s"] * len(values))
        # Exclude 'id' from the column list
        columns = ", ".join(row.keys())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, values)
        db.commit()
        print(f"✅ Inserted row: {values} at {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error inserting data: {e} at {time.strftime('%H:%M:%S')}")

    # 6️⃣ Wait 3 minutes before next insert
    time.sleep(180)
    