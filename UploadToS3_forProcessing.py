#!/Users/davidmar/opt/anaconda3/bin/python3
import boto3
import os

s3 = boto3.resource("s3")
bucket_name = 'davidmar.test'
folder_path = './s3_upload_directory'

bucket = s3.Bucket(bucket_name)

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)
        with open(file_path, 'rb') as data:
            bucket.upload_file(file_path, filename)


