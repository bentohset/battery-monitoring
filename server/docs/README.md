# Backend Flask Documentation

Routes packet format
```
{
    "message": String
}, status_code
```

Status Codes
|Code |Description |
|:----|:---------- |
|200  |Sucess |
|500  |Internal server error unhandled |
|400  |Bad request: server cannot request due to client error |
|401  |Unauthenticated: client must authenticate to get a response |
|403  |Forbidden: client no access rights (identity is known) |
|404  |cannot find the requested resource, url not recognised |


# TODO

- azure data pipeline test with sample module
    - create new table in psql




# MS Azure Documentation:

Modules (sensors) -> IoT Edge Runtime (local remote server) -> IoT Hub (Cloud) <- User access

On edge: run on terminal/powershell as admin
`Connect-EflowVm`
- turns on and connect to the virtual machine which runs the runtime
`sudo iotedge list`
- get list of iot modules connected
`sudo iotedge logs <ModuleName> -f`
- gets logs of messages received from iot module named
`exit`
- exits the vm

`az iot hub device-identity connection-string show --device-id <EdgeName> --hub-name <HubName>`
- shows connection string for provisioning
`Provision-EflowVm -provisioningType ManualConnectionString -devConnString <STRING>`
- provision with connection string
`az group create --name IoTEdgeResources --location southeastasia`
- creates azure resource group
`az iot hub create --resource-group IoTEdgeResources --name <HubName> --sku F1 --parition-count 2`
- creates the iot hub with respect to resource group
- each subscription can only have one free hub (change SKU to S1)


# PostgreSQL Setup

1. Install PostgreSQL
    - Create password for superuser for your local computer
2. Setup Environment Variables
    - Go to computer environment variables
    - Edit `Path`
    - New paths and add the following paths
    - `C:\Program Files\PostgreSQL\15\bin` and `C:\Program Files\PostgreSQL\15\lib`
    - or wherever the local file is stored on your device
3. Run Powershell with adminitrator
    - input `psql postgres postgres`
    - prompted for password (from during installation)
    - will be logged in as user postgres
4. Disable 3rd party antivirus and use native firewall settings
    - add inbound rule to enable tcp on port 5432

## `psql` Common Commands

- `\du` list of all users
- `\l` list all databases
- `\c <db_name>` switch to another database
- `\dt` list all database tables
- `\d <table_name>` see table structure
- `\q` quit psql
- `psql -d <db_name> -U <username> -W` connect to db on the same host
- `psql -h <hostname> -p <port> -U <username> -d <database> -W` connect to db on different host
    - username: `postgres` for superuser
    - database: `battery_monitoring`
    - port: `5432` default port
    - hostname: ip address of remote server
    - `-W`: prompts for password


URI Connection string: `postgresql//<username>:<password>@<hostname>:<port>/<database>`