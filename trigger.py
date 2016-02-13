import boto3
import json

with open('config/config.json') as config:
    data = json.load(config)

def trigger(event, context):
    # Get IP addresses of EC2 instances
    ec2 = boto3.client('ec2')
    instDict = ec2.describe_instances(
            Filters = data['trigger']['ec2']['filters']
        )

    hostList = []

    for r in instDict['Reservations']:
        for inst in r['Instances']:
            hostList.append(inst['PublicIpAddress'])

    # Invoke worker function for each IP address
    awsLamba = boto3.client('lambda')
    for host in hostList:
        print "Invoking worker_function on " + host
        invokeResponse = awsLamba.invoke(
            FunctionName = data['trigger']['lambda']['function']['name'],
            InvocationType = 'Event',
            LogType = 'Tail',
            Payload = '{"IP":"'+ host +'"}'
        )
        print invokeResponse

    return{
        'message' : "Trigger function finished"
    }
