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


