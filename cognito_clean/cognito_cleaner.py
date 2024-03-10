import boto3
import pytz
from datetime import datetime
from cognito_clean.cognito_manager import process_unconfirmed_users
from cognito_clean.file_manager import write_deleted_users_to_s3
from cognito_clean.notification_service import send_email_notification

cognito_client = None
s3_client = None
sns_client = None

# Caching the last processed time and deleted users
last_processed_time_cache = {}
deleted_users_cache = set()

def main_handler(event, context):
    global cognito_client, s3_client, sns_client

    # Extract configuration from event
    aws_region = event.get('aws_region', '')
    cognito_user_pool_id = event.get('cognito_user_pool_id', '')
    s3_bucket_name = event.get('s3_bucket_name', '')
    s3_key = event.get('s3_key', '')
    sns_topic_arn = event.get('sns_topic_arn', '')
    aged_user_threshold_minutes = event.get('aged_user_threshold_minutes', '10080')
    user_status = event.get('user_status', 'UNCONFIRMED')
    delete_enabled = event.get('delete_enabled', 'False').lower() == 'true'

    # Initialise the Boto3 clients with the region from the event
    cognito_client = boto3.client('cognito-idp', region_name=aws_region)
    s3_client = boto3.client('s3', region_name=aws_region)
    sns_client = boto3.client('sns', region_name=aws_region)

    current_run_time = datetime.now(pytz.utc)
    
    # Process unconfirmed users and get the list of deleted usernames and user objects
    deleted_usernames, deleted_user_objects = process_unconfirmed_users(
        cognito_client,
        cognito_user_pool_id,
        aged_user_threshold_minutes,
        user_status,
        delete_enabled,
        last_processed_time_cache,
        deleted_users_cache
    )
    
    # Print the list of deleted usernames
    print(f"Deleted users: {deleted_usernames}")

    if deleted_user_objects:
        # Write the list of deleted user objects to S3 in JSON format
        write_deleted_users_to_s3(s3_client, deleted_user_objects, s3_bucket_name, s3_key)
        
        # Send an email notification with the list of deleted user objects
        send_email_notification(sns_client, sns_topic_arn, deleted_user_objects)
        message = "Deleted users were processed and notifications were sent."
        
        # Update the last_processed_time_cache with the current run time only if users were deleted
        last_processed_time_cache[cognito_user_pool_id] = current_run_time
    else:
        message = "No unconfirmed users to delete or delete not enabled."
    
    return {
        'statusCode': 200,
        'body': message
    }

if __name__ == '__main__':
    event = {}
    context = {}
    main_handler(event, context)