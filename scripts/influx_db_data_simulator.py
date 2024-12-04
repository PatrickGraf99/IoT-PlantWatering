from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time
import os
from dotenv import load_dotenv


load_dotenv()

# Configuration, all changes here must also be made in docker.yml
url = "http://localhost:8086"  # InfluxDB URL
token = os.getenv("INFLUXDB_API_TOKEN") 
org = "iot"                    # Organization name
bucket = "iot-data"            # Bucket name

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Simulate data for a single plant
plant_names = ["Efeutute", "Monstera", "Ficus"]

def generate_data(plant_name):
    point = (
        Point("plant_data")
        .tag("plant_name", plant_name)
        .field("ground_moisture", random.uniform(20, 80))  # Simulated soil moisture
        .field("air_moisture", random.uniform(30, 70))     # Simulated air humidity
        .field("temperature", random.uniform(20, 35))      # Simulated temperature
        .time(int(time.time() * 1e9))  # Current timestamp in nanoseconds
    )
    return point

# Write data every 5 seconds (adjust as needed)
try:
    print("Starting data simulation...")
    while True:
        for plant_name in plant_names:
            data_point = generate_data(plant_name)
            write_api.write(bucket=bucket, org=org, record=data_point)
            print(f"Data written: {data_point}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Simulation stopped.")
finally:
    client.close()