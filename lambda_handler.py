import boto3
import config
import pytz
from datetime import datetime
from library.cognito_manager import list_users, delete_users
from library.file_manager import write_deleted_users_to_s3
from library.notification_service import send_email_notification

# Initialize the Boto3 clients and environment variables
cognito_client = boto3.client('cognito-idp', region_name=config.aws_region)
s3_client = boto3.client('s3', region_name=config.aws_region)
sns_client = boto3.client('sns', region_name=config.aws_region)

# Caching the last processed time and deleted users
last_processed_time_cache = {}
deleted_users_cache = set()

def main_handler(event):
    current_run_time = datetime.now(pytz.utc)
    delete_enabled = event.get('delete_enabled', 'false').lower() == 'true'
    
    # List all unconfirmed users, considering the last processed time from the cache
    unconfirmed_users = list_users(cognito_client, config.cognito_user_pool_id, config.aged_user_threshold_minutes, config.user_status, last_processed_time_cache)
    
    # Print the list of unconfirmed users
    print(f"{config.user_status} users older than {config.aged_user_threshold_minutes} minutes: {unconfirmed_users}")

    # Delete the unconfirmed users and collect the ones successfully deleted
    deleted_users = [user for user in unconfirmed_users if delete_users(cognito_client, config.cognito_user_pool_id, user, delete_enabled, deleted_users_cache)]

    if deleted_users:
        # Write the list of deleted users to S3
        write_deleted_users_to_s3(s3_client, deleted_users, config.s3_bucket_name, config.s3_key)
        # Send an email notification with the list of deleted users
        send_email_notification(sns_client, config.sns_topic_arn, deleted_users)
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
    main_handler(event)

