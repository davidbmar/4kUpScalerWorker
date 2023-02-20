#!/invokeai/.venv/bin/python3
##!/Users/davidmar/opt/anaconda3/bin/python3
#queue_url = sqs.get_queue_url(QueueName='davidmar-test-sqs-queue')['QueueUrl']
#
import boto3
import json
import os

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
    print ("python /4kUpScalerWorker/Real-ESRGAN/inference_realesrgan.py -n RealESRGAN_x4plus -i s3_download_directory/"+object_key+" -o processed_directory") 
    stream = os.popen("python /4kUpScalerWorker/Real-ESRGAN/inference_realesrgan.py -n RealESRGAN_x4plus -i s3_download_directory/"+object_key+" -o processed_directory") 
    output=stream.read()
    print (output)

#    # now upload to the S3 bucket.
#    source_filename=full_path_output_filename
#    bucket="davidmar.test.upscaled"
#    target_key="processed."+object_key
#    s3.upload_file(source_filename,bucket,target_key)
#

    # Delete the message from the SQS queue
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

