# Author : Vibhum Chandorkar (vich1161@colorado.edu)
# Name : Lab 2
# Purpose : obj 5.4
# Date : 2/4/2019
# Version : 3

import smtplib
import time
from boto3.session import Session
from datetime import datetime, timedelta
from operator import itemgetter


# Creating a Session
session = Session(
    aws_access_key_id='****',
    aws_secret_access_key='*****',
    region_name='us-west-1')

# Connecting session to cloudwatch and EC2
cw = session.client('cloudwatch')
ec2 = session.resource('ec2')

# creating a infinite while loop for continuously fetching the data
while True:
    ids = []

    # Fetching the IDs of the instances and putting them in ids list
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        ids.append(instance.id)

    # Removing the ID of two orginially created instances
    ids.remove('i-06cf88d26bea831fd')
    ids.remove('i-0b12e7b18a20101bf')

    id = []

    # Creating a for loop for fetching the CPU Utilization of each ID
    for idss in ids:
        id.append(idss)
        a = []

        # Creating id1 because while terminating the instance it only accepts list type
        id1 = [id[0]]

        print('The Instance ID is ' + str(idss))

        # Fetching the CPU Utilization data
        results = cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': id[0]}],
            StartTime=datetime.utcnow() - timedelta(minutes=25),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=['Average'])

        datapoints = results['Datapoints']

        last_datapoint = sorted(datapoints, key=itemgetter('Average'), reverse=True)
        print(last_datapoint)

        
        for i in last_datapoint:
            a.append(i['Average'])
        print(a)

        # taking the Average of all the data found at various time period
        b = (sum(a)) / len(a)
        print(b)

        # Comparing the average to a threshold
        if int(b) < int(1):

            # Emailing the admin
            msg = 'Instance with the ID ' + str(idss) + ' has been terminated and a new instance will be created'
            fromaddr = 'vibhumchandorkar@gmail.com'
            toaddr = 'vich1161@colorado.edu'
            username = 'vibhumchandorkar@gmail.com'
            password = 'xxxx'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddr, msg)
            server.quit()

            # Terminating the Instance
            ec2.instances.filter(InstanceIds=id1).terminate()

            # It takes time for the updating mechanism to take place and therefor stoping the script
            time.sleep(300)

            # Creating a new Instance
            ec2.create_instances(ImageId='ami-0ad16744583f21877', MinCount=1, MaxCount=1)
            time.sleep(300)

            print('The Instance with ID ' + str(idss) + ' has been terminated')
        pass
