# Installation


```
python3 -m pip install virtualenv
python3 -m vevn venv
# source vevn
source ./venv/bin/activate
# install requirements
python -m pip install -r requirement.txt
```

Create a bash file to source env
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
python main log/file_name.log
```

## Grafan Dashboard
import grafana_dashboard.json to create dashboard on grafa