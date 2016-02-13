import boto3
import paramiko
import json

with open('config/config.json') as config:
    data = json.load(config)

def worker(event, context):

    s3_client = boto3.client('s3')

    # Download private key file from secure S3 bucket
    s3_client.download_file('s3-key-bucket','keys/keyname.pem', '/tmp/keyname.pem')

    k = paramiko.RSAKey.from_private_key_file("/tmp/keyname.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host=event['IP']
    print "Connecting to " + host
    c.connect( hostname = host, username = "ubuntu", pkey = k )
    print "Connected to " + host

    commands = [
        "aws s3 cp s3://s3-bucket/scripts/HelloWorld.sh /home/ec2-user/HelloWorld.sh",
        "chmod 700 /home/ec2-user/HelloWorld.sh",
        "/home/ec2-user/HelloWorld.sh"
        ]
    for command in commands:
        print "Executing {}".format(command)
        stdin , stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }
