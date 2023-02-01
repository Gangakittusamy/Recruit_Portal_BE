import boto3
from botocore.client import BaseClient

#S3 connection using Access && Secret key
def s3_auth() -> BaseClient:
    s3 = boto3.client(service_name='s3', aws_access_key_id='AKIAWX3Y35NCLYYLSVPM',
                      aws_secret_access_key='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'
                      )

    return s3
