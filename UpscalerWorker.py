#!/invokeai/.venv/bin/python3
##!/Users/davidmar/opt/anaconda3/bin/python3
#queue_url = sqs.get_queue_url(QueueName='davidmar-test-sqs-queue')['QueueUrl']
#
import boto3
import json
import os
import subprocess
from s3_utils import upload_file_to_s3

# Create an SQS client and s3 client.
sqs = boto3.client('sqs')
s3 = boto3.client('s3')


# Get the URL of the SQS queue
queue_url = sqs.get_queue_url(QueueName='davidmar-test-sqs-queue')['QueueUrl']

# Receive messages from the SQS queue
response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

# Process the messages
for message in response.get('Messages', []):
    # Extract the S3 event from the message body
    event = json.loads(message['Body'])

    # Extract the information about the S3 object from the event
    s3_object = event['Records'][0]['s3']
    bucket_name = s3_object['bucket']['name']
    object_key = s3_object['object']['key']

    # Process the S3 object (e.g., copy it to another location)
    print ("bucket_name:"+bucket_name)
    print ("object_key:"+object_key)

    # Download the S3 object
    file = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = file['Body'].read()

    # Write the object contents to a local file
    prefix="./s3_download_directory/"
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    with open(prefix+object_key, "wb") as f:
        f.write(file_content)
    f.close()

    # Processing on the file.
    # Now do some processing on this file.
    input_prefix="./s3_download_directory/"
    output_prefix="./processed_directory/"
    if not os.path.exists(input_prefix):
        os.makedirs(output_prefix)
    if not os.path.exists(output_prefix):
        os.makedirs(output_prefix)

    full_path_input_filename=input_prefix+object_key
    full_path_output_filename=output_prefix+"processed."+object_key
    print("input_filename:"+full_path_input_filename)
    print("output filename:"+full_path_output_filename)

##Usage: python inference_realesrgan.py -n RealESRGAN_x4plus -i infile -o outfile [options]...
    command="/invokeai/.venv/bin/python /4kUpScalerWorker/Real-ESRGAN/inference_realesrgan.py -n RealESRGAN_x4plus -i s3_download_directory/"+object_key+" -o processed_directory" 
    print (command)
    try:
        output = subprocess.check_output(command, shell=True) # note this is a security hole.
    except subprocess.CalledProcessError as e:
        raise Exception(f'command failed with return code {e.returncode}: {e.output.decode()}')
    print (output.decode())

    print ("Completed Image processing\n")
###############################################
# Now upload to the S3 bucket.
###############################################
    # set the directory path and filename of the file to be uploaded
    file_path = output_prefix + object_key 
    
    # set the S3 bucket name and key where the file will be uploaded
    bucket_name = "davidmar.test.upscaled"
    key_name = object_key 
    
    # upload the file to the S3 bucket
    upload_file_to_s3(file_path, bucket_name, key_name)

###############################################
# Now assuming all worked properly you want to delete from the SQS queue.
###############################################
    
    # Delete the message from the SQS queue
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])


