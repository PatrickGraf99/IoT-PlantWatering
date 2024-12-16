@echo off
REM Starting InfluxDB and Grafana, this could take some time
docker-compose up -d
echo Startup complete
pause

