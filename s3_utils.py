import boto3
from botocore.exceptions import ClientError

def upload_file_to_s3(file_path, bucket_name, key_name):
    """
    Upload a file to an S3 bucket.
    """
    # create an S3 client
    s3 = boto3.client('s3')

    try:
        # upload the file to the S3 bucket
        s3.upload_file(file_path, bucket_name, key_name)
    except ClientError as e:
        # log any errors that occur during the upload process
        print(f"Error uploading file {file_path} to S3 bucket {bucket_name}: {e}")
        return False
    return True
