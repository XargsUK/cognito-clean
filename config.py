import os

aws_region = os.getenv('AWS_REGION', '')
cognito_user_pool_id = os.getenv('COGNITO_USER_POOL_ID', '')
s3_bucket_name = os.getenv('S3_BUCKET_NAME', '')
s3_key = os.getenv('S3_KEY', '')
sns_topic_arn = os.getenv('SNS_TOPIC_ARN', '')
aged_user_threshold_minutes = os.getenv('AGED_USER_THRESHOLD_MINUTES', '1')
user_status = os.getenv('USER_STATUS', 'UNCONFIRMED,RESET_REQUIRED,FORCE_CHANGE_PASSWORD')
delete_enabled = os.getenv('DELETE_ENABLED', 'False')