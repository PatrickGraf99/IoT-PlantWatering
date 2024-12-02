@echo off
REM Start Docker Compose containers (Grafana and InfluxDB)
docker-compose up -d

REM Wait for Grafana and InfluxDB to be ready (adjust the timeout if necessary)
echo "Waiting for Grafana to start..."
timeout /t 30

REM Check if it's the first startup by looking for the 'first_start.txt' file in Grafana data folder
IF NOT EXIST "data/grafana/first_start.txt" (
    REM First startup - Copy the YAML files into the Grafana provisioning directory
    echo "First startup - importing datasources and dashboards..."

    REM Copy datasources.yaml and dashboards.yaml to the correct location for provisioning
    copy provisioning/datasources.yaml ./data/grafana/provisioning/datasources/datasources.yaml
    copy provisioning/dashboards.yaml ./data/grafana/provisioning/dashboards/dashboards.yaml

    REM Create the 'first_start.txt' file to mark the first startup as completed
    echo "First startup complete" > "data/grafana/first_start.txt"
) ELSE (
    echo "Subsequent startup - skipping import."
)

REM Optional: You can add additional commands to initialize or check the system state
echo "Grafana and InfluxDB are now running."

REM End of script