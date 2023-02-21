# 4kUpScalerWorker
The idea behind this is to 4k upscale a given picture.

Pictures can be put to an S3 bucket.

When that picture is PUT into the bucket, it then creates an event
which adds this to an SQS queue.

The client then pulls the picture off the queue, upscales it
And moves it to a processed directory.

This helps me spawn workers given an S3 directory.
When the S3 directory has a PUT to it, then it puts this to a SQS Queue.
The Queue then can be pulled from a worker.

# Run Procedure
To set this up do the following steps.
1.  Open up runpod.io
2.  Select the invokeAi image
3.  git clone https://github.com/davidbmar/4kUpScalerWorker.git

For the time being setup the creds.  This is temporary, until I build a signed URL.
go to /root
mkdir .aws
copy in : config and credentials.
But ultimately, you need access to pull off the SQS queue, and pull from the S3 buckets.

For git to checkin you will also want to have a token for git hub.
git remote set-url origin https://<<USERNAME>>:<<TOKEN>>@github.com/davidbmar/4kUpScalerWorker.git
