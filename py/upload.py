from secrets import access_key, secret_access_key
import boto3
import os

client = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key)


for file in os.listdir():
    print("Loading "+str(file))
    if '.py' in file or '.db' in file:
        print("Loading "+str(file))
        upload_file_bucket = 'traffic-bolzen'
        upload_file_key = 'python/' + str(file)
        client.upload_file(file, upload_file_bucket, upload_file_key)
