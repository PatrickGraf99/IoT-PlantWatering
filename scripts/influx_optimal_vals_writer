from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time
import os
import json
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

with open("config/thresholds.json", "r") as file:
    data = json.loads(file.read())

# print(data["plants"])

plants_data = data["plants"]

try:
    for plant_name, thresholds in plants_data.items():
        point = (
            Point("optimal_conditions")
            .tag("plant_name", plant_name)
            .field("optimal_temp_min", thresholds["optimalTempMin"])
            .field("optimal_temp_max", thresholds["optimalTempMax"])
            .field("optimal_air_moisture_min", thresholds["optimalAirMoistureMin"])
            .field("optimal_air_moisture_max", thresholds["optimalAirMoistureMax"])
            .field("optimal_ground_moisture_min", thresholds["optimalGroundMoistureMin"])
            .field("optimal_ground_moisture_max", thresholds["optimalGroundMoistureMax"])
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Optimal data written for plant: {plant_name}")
except Exception as e:
    print(f"Error writing optimal data: {e}")
finally:
    client.close()