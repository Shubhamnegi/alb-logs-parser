import boto3
import os
import gzip
import io


# Configure the AWS credentials and region
aws_access_key_id =  os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
aws_region = os.getenv('AWS_REGION')

# Create an S3 client
s3 = boto3.client('s3',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=aws_region)


def read_from_bucket(bucket_name,file_key):
    """
    To unzip and read payload from s3 bucket
    """
    # Read the object data from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    gzip_file_object = response['Body'].read()    
    with gzip.GzipFile(fileobj=io.BytesIO(gzip_file_object)) as gzip_file:
        line = gzip_file.readline()
        while(line):            
            yield line
            line = gzip_file.readline()
    

