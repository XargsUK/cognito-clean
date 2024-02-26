import os

# AWS Region where the Lambda is deployed
aws_region = os.getenv('AWS_REGION', '')

# Cognito User Pool ID 
cognito_user_pool_id = os.getenv('COGNITO_USER_POOL_ID', '')

# S3 bucket name where the list of deleted users will be stored
s3_bucket_name = os.getenv('S3_BUCKET_NAME', '')

# S3 key (path) for storing the list of deleted users
s3_key = os.getenv('S3_KEY', '')

# SNS Topic ARN for sending email notifications
sns_topic_arn = os.getenv('SNS_TOPIC_ARN', '')

# Threshold in minutes to determine the age of users to be considered for deletion
aged_user_threshold_minutes = os.getenv('AGED_USER_THRESHOLD_MINUTES', '10080')

# Comma-separated list of user statuses to filter users in Cognito
user_status = os.getenv('USER_STATUS', 'UNCONFIRMED')

# Flag to enable or disable the deletion of users
delete_enabled = os.getenv('DELETE_ENABLED', 'False')
