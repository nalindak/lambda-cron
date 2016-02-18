import boto3
import os

# Private method to get public DNS name for instance with given tag key and value pair
def _get_public_dns(value):

    # Array of public IP addresses
    hostList = []

    # Get IP addresses of EC2 instances
    ec2 = boto3.client('ec2')

    # Get instances Dict
    instDict = ec2.describe_instances(
            Filters = [
                {
                    "Name": "tag:Name",
                    "Values": [
                        value
                    ]
                }
            ]
        )

    # Populate hostList with IP addresses
    for r in instDict['Reservations']:
        for inst in r['Instances']:
            hostList.append(inst['PublicDnsName'])

    return hostList

print(_get_public_dns('something'))
