import boto3
from botocore.exceptions import ClientError
from config import Config
s3 = boto3.client(
's3',
aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
region_name=Config.AWS_REGION
)
def upload_file(file_path, key, extra=None):
extra = extra or {}
try:
s3.upload_file(file_path, Config.S3_BUCKET, key, ExtraArgs=extra)
return f"s3://{Config.S3_BUCKET}/{key}"
except ClientError as e:
raise RuntimeError(str(e))
def generate_presigned_url(key, expiration=3600):
return s3.generate_presigned_url(
'get_object',
Params={'Bucket': Config.S3_BUCKET, 'Key': key},
ExpiresIn=expiration
)
