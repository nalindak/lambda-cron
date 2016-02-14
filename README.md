# lambda-cron
Run Cron Jobs via Python

- Trigger function
* create lambda function and select lambda-canary
* on the "Configure event sources" page, "Event source type" defaults to "Scheduled Event".
* under "Schedule expression" select the interval
* copy and paste the trigger function
* specifiy the file name and the handler as "trigger.trigger"
* select the "lambda-role" here you have to create IAM role having permission to assume role and EC2 describe permissions

- Worker function
```sh
pip install virtulenv
virtualenv –p /usr/bin/python2.7 path/to/worker.py
source path/to/worker/bin/activate
pip install pycrypto
pip install paramiko
zip path/to/zip/worker.zip worker.py

cd path/to/worker/lib/python2.7/site-packages
zip –r path/to/zip/worker.zip
```

* upload file "health.sh" with following content,

```sh
# Get instanceId
instanceid=`wget -q -O - http://instance-data/latest/meta-data/instance-id`
LOGFILE="/home/ec2-user/$instanceid.$(date +"%Y%m%d_%H%M%S").log"

# Run Hi and redirect output to a log file
echo "Hi $instanceid" > $LOGFILE

# Copy log file to S3 logs folder
aws s3 cp $LOGFILE s3://s3-bucket/logs/
```

* upload the .pem file to s3 bucket (make sure only the lambda worker can only access this file)

