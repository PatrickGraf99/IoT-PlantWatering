from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

# Configuration
url = "http://localhost:8086"  # InfluxDB URL
token = "FjnVIivUwZ01ZWhbqzEU0SQGkmY2L7oQX3xwtBUPMhwEZwefV-AjsLkhzG-kfNAAtSj-tay3qTVMdV7E93j9DQ=="     # Replace with your admin token
org = "iot"                    # Organization name
bucket = "iot-data"            # Bucket name

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Simulate data for a single plant
plant_name = "Efeutute"

def generate_data():
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
        data_point = generate_data()
        write_api.write(bucket=bucket, org=org, record=data_point)
        print(f"Data written: {data_point}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Simulation stopped.")
finally:
    client.close()