# Objective
To push alb log to influxdb. Influxdb data can be used to plot charts on granana, which allows easy analysis of request patterna and create alerts.

# Open points
- Can be modified to work and lambda function. On every s3 write of alb log lambda can be triggered to process log and push to influx. This will allow near real time data for request analysis.


# Installation

```
python3 -m pip install virtualenv
python3 -m vevn venv
# source vevn
source ./venv/bin/activate
# install requirements
python -m pip install -r requirement.txt
```

Create a bash file to source env. You can also use any other method to push env variable. 
```
touch cred.bash
echo "export INFLUX_DB_HOST=repalce_with_url" >> cred.bash
echo "export INFLUX_DB_USER=replace_with_username" >> cred.bash
echo "export INFLUX_DB_PASSWORD=replace_with_password" >> cred.bash

source cred.bash
```

Download logs
```
mkdir logs
aws s3 cp s3://path_to_logs logs --recursive  # download logs in logs dir
gzip -dr logs # unzip all logs
```

Send logs
You can use xargs to list file name and pass directly to main file. Example for 1 log file is below
```
# To parse logs in a directory
python main.py -d ./logs/

# To parse one file
python main.py -f ./logs/file.log
```

## Grafan Dashboard
import grafana_dashboard.json to create dashboard on grafa
