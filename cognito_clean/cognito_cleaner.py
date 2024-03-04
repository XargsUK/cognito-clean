import boto3
import config
import pytz
from datetime import datetime
from library.cognito_manager import process_unconfirmed_users
from library.file_manager import write_deleted_users_to_s3
from library.notification_service import send_email_notification

# Initialize the Boto3 clients with the region from the config
cognito_client = boto3.client('cognito-idp', region_name=config.aws_region)
s3_client = boto3.client('s3', region_name=config.aws_region)
sns_client = boto3.client('sns', region_name=config.aws_region)

# Caching the last processed time and deleted users
last_processed_time_cache = {}
deleted_users_cache = set()

def main_handler(event, context):
    current_run_time = datetime.now(pytz.utc)
    delete_enabled = config.delete_enabled.lower() == 'true'
    
    # Process unconfirmed users and get the list of deleted usernames and user objects
    deleted_usernames, deleted_user_objects = process_unconfirmed_users(
        cognito_client,
        config.cognito_user_pool_id,
        config.aged_user_threshold_minutes,
        config.user_status,
        delete_enabled,
        last_processed_time_cache,
        deleted_users_cache
    )
    
    # Print the list of deleted usernames
    print(f"Deleted users: {deleted_usernames}")

    if deleted_user_objects:
        # Write the list of deleted user objects to S3 in JSON format
        write_deleted_users_to_s3(s3_client, deleted_user_objects, config.s3_bucket_name, config.s3_key)
        
        # Send an email notification with the list of deleted user objects
        send_email_notification(sns_client, config.sns_topic_arn, deleted_user_objects)
        message = "Deleted users were processed and notifications were sent."
        
        # Update the last_processed_time_cache with the current run time only if users were deleted
        last_processed_time_cache[config.cognito_user_pool_id] = current_run_time
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