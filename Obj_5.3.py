# Author : Vibhum Chandorkar (vich1161@colorado.edu)
# Name : Lab 2
# Purpose : obj 5.3
# Date : 2/4/2019
# Version : 3

from datetime import datetime, timedelta
from operator import itemgetter
from boto3.session import Session

# creating an empty lists
ids = []
a = []
final_list = []

# Creating a session
session = Session(
    aws_access_key_id='*****',
    aws_secret_access_key='****',
    region_name='us-west-1')

# Creating CloudWatch and EC2 session
cw = session.client('cloudwatch')
ec2 = session.resource('ec2')

# Extracting the Instance Ids from the list
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    ids.append(instance.id)

# Selecting one Instance ID from the list
id = ids[0]

# Defining a list of metrics
metrics = ['StatusCheckFailed', 'CPUUtilization', 'NetworkIn', 'NetworkOut']

# Creting a for loop and fetching the details regarding each metric
for metric in metrics:
    results = cw.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric,
        Dimensions=[{'Name': 'InstanceId', 'Value': id}],
        StartTime=datetime.utcnow() - timedelta(minutes=30),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average'])

    datapoints = results['Datapoints']

    last_datapoint = sorted(datapoints, key=itemgetter('Average'), reverse=True)

    for i in last_datapoint:
        a.append(i['Average'])

    b = (sum(a))/len(a)
    final_list.append(b)

# Printing the required results
print("Instance ID: " + str(id))
print("Status Check: " + str(final_list[0]))
print("CPU Utilization: " + str(final_list[1]))
print("NetworkIN: " + str(final_list[2]))
print("NetworkOut: " + str(3))
