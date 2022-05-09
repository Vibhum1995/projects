
# Purpose : AWS
# Date : 02/24/2019
# Version : 3.0

from time import *
from boto3.session import Session
import pytz, datetime
from botocore.exceptions import ClientError
from prettytable import PrettyTable


def s3Bucket(bucket_name):
    # Creating a AWS session
    session = Session(
        aws_access_key_id='*****',
        aws_secret_access_key='*****',
        region_name='us-west-1')

    # Connecting to S3
    s3 = session.client('s3')
    s3_resource = session.resource('s3')

 
    # Creating a time stamp and adding to the filename
    time_stamp = datetime.datetime.now()
    print(time_stamp)
    print(type(str(time_stamp)))
    add_time = str(time_stamp)
    file_name = 'batman_'+add_time+'.txt'
    file_plot = 'Plot_'+add_time+'.png'

    # Uploading files to S3
    s3.upload_file('batman.txt', bucket_name,file_name)
    s3.upload_file('Plot.png', bucket_name,file_plot)

    # Creating the bucket identifier and print bucket name
    id = s3.list_objects_v2(Bucket=bucket_name)
    print(id)
    print('Bucket:', id['Name'])

    # Checking if there are any contents in the list
    content_list =[]
    if 'Contents' in id:
        # If contents presesnt the printing the contents
        for indices in range(len(id['Contents'])):
            contents = id['Contents'][indices]['Key']
            content_list.append(contents)

        # Putting the contents in Pretty table
        x = PrettyTable()
        x.add_column("Files", content_list)
        print(x)
        print('\n')

        # Comparing time (Have converted both the current and last modified time to UTC format)
        for indices in range(len(id['Contents'])):
            contents = id['Contents'][indices]['Key']
            current_time = datetime.datetime.utcnow()
            current_time1 = current_time.strftime("%Y-%m-%d %H:%M:%S")
            time = (id['Contents'][indices]['LastModified'])
            time1 = time.astimezone(pytz.utc)
            new = (time1 + datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

            # Deleting if the contents have last modified  more than 5 minutes
            if current_time1 > new:
                s3.delete_object(Bucket=bucket_name, Key=contents)
                print('Due to 5 minutes age, content ('+contents+') has been deleted')

        print('\n')

    # If there are no contents
    else:
        print('No contents to show')
