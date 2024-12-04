@echo off
REM Start Docker Compose containers (Grafana and InfluxDB)
echo "Starting up Grafana and InfluxDB, this could take some time"
docker-compose up -d
echo "Startup complete"
pause

