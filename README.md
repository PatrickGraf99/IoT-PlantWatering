# Installation of the system on a new machine

This guide will lead you through the installation of the system on a new machine. All tests were done on Windows machines, a guide for Linux may follow

## Step 1: Clone this repository

Clone this repository on your drive. For demonstration purposes we will assume the path to be C:/IOT-PlantWatering. Replace this with the path you chose 
when cloning. You will receive a .env file from a trusted source. Place the .env file in the root directory of the project. You will see an overview of the filestructure further down this guide. Since everything will run locally, you can safely change values in your .env file. This is however not recommended since it can occur, that some values are hardcoded in other files, leading to errors.

## Step 2: Install needed programs
It is assumed that Python is already installed on your device. If not, install python.

### Step 2.1: Install VS Code
VS Code is used to edit/run files and supports all of the file formats used. You can use any Editor you want though.

### Step 2.2: Install Docker
Docker is used to deploy Grafana and InfluxDB. We used [Docker Desktop](https://www.docker.com/products/docker-desktop/). Install and create an account/login. Everything
needed for Grafana and InfluxDB to run will automatically be setup later on.

### Step 2.3: Insall python-dotenv and influxdb-client for simulating data
Open the scripts directory (either in VS Code or the command prompt) and use pip install python-dotenv and pip install influxdb-client to install the modules used for data
simulation (This can be skipped if real sensor data is available).

## Step 3: Initial startup
Open the command prompt and navigate to C:/IOT_PlantWatering. run the command "docker-compose up -d" after making sure that docker desktop is running. Alterbatively to using cmd you can execute the start-docker.bat by double-clicking it. Docker should now install needed stuff for InfluxDB and Grafana. This may take some time.

### Step 3.1: Checking for InfluxDB
After the setup is done open a browser of your choice and navigate to http://localhost:8086/ which should bring up the InfluxDB UI. You can lookup the username and password in your .env file. 

#### Step 3.1.1: Ensuring it works
In the InfluxDB UI navigate to load data -> API tokens. Generate a new API Token or clone the admins token. In either case, copy the token and place it inside your .env file INFLUXDB_API_TOKEN=token. Do not include any spaces. After this step you can run the influx_data_simulator.py inside the scripts directory. To do so use VS Code or
the command prompt. After waiting a few minutes head back to the InfluxDB UI and navigate to Data Explorer. Make a new query using iot-data as bucket and filtering by plant_data. After clicking on submit data should show up in the graph view. You can hover over it to see what data was inserted by the simulator.

### Step 3.2 Checking for Grafana
In your browser navigate to http://localhost:3000/ which should bring up the Grafana UI. The login data should be admin as both username and password.

#### Step 3.2.1 Setting up a connection between Grafana and Influx
In the Grafana UI navigate to Connections -> DData sources and clicke on "Add data source". From the list select influxdb.
Set up this source using the following parameters
| Parameter | Value |
| --- | --- |
| name | InfluxDB |
| Query Language | Flux |
| URL | http://influxdb:8086 |
| Organization | name of your org in influx (default: iot) |
| Token | The token you got in Step 3.1.1 |
| Min time interval | 10s |

You can leave the rest as is. Clicking on "Save & test" should display a success notification.

#### Step 3.2.2 Setting up a dashboard
To see data in Grafana a dashboard is needed. Go to Dashboards and click on "New", then select "Import". Import the .json file from IOT_PlantWatering/provisioning/dashboards. Click on import.
After that a dashboard named "Plant Data Display" should show up. Open it by clicking on it.

## Troubleshooting
The Python Script doesn't work - Make sure all needed libraries are installed using pip. Also make sure you set the correct token in your .env file since it will be used to quthorize writing data to Grafana. 
Grafana/InfluxDB are not loading - Check if Docker is started
Docker doesn't work - Ensure that Docker Desktop is running
The data source is not working - Check if you used the correct values in your setup.
I don't see any data in Grafana - Use the InfluxDB UI to check if there is actual data in the database. Use the simulator to simulate data
Data is in the database and the connetion works, but I can't see anything in Grafana - In your dashboard click on the 3 dots in the top right corner of one of the timelines and click on edit. Make sure InfluxDB is selected as data source and the query is correct. Set the display time to Last 15 minutes and try refreshing manually. Also check wheter the textbox on top contains a plant name. If not you can enter Efeutute to test

Your file structure after running the docker for the first time should look something like this

iot-plantwatering/
├── .env                         # Environment variables for the project
├── .gitignore                   # Ignored files and directories
├── README.md                    # Documentation for the project
├── docker-compose.yml           # Docker Compose configuration
├── scripts/                     # Directory for the simulation script
│   └── influx_data_simulator.py # Plant data simulation script
├── provisioning/                # Grafana provisioning files
│   ├── dashboards/              # Dashboards provisioning folder
│   │   ├── dashboards.yml       # Dashboard provisioning config
│   │   └── dashboard.json       # Example exported dashboard JSON
├── data/                        # Persistent data storage for Grafana and InfluxDB
│   ├── grafana/                 # Grafana persistent storage
│   └── influxdb/                # InfluxDB persistent storage



# Understanding the Hardware
The used Hardware will be documented. WIP. 

# Following the installation
After making changes to the dashboard, should you plan on publishing these changes, it is neccessary that you click on share -> Export -> save to file and create a new .json file in IOT-PlantWatering/provisioning/dashboards.

All changes you make are only local! Data on your machine will not be shared, same for dashboards, data sources etc. 

A system to import data sources and dashboards automatically is planned if enough time is left at the end of the project.