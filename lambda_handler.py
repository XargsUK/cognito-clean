import boto3
from library import *
from config import *
from datetime import datetime
import pytz

# Initialize the Boto3 clients and environment variables
cognito_client = boto3.client('cognito-idp', region_name=aws_region)
s3_client = boto3.client('s3', region_name=aws_region)
sns_client = boto3.client('sns', region_name=aws_region)

# Caching the last processed time and deleted users
last_processed_time_cache = {}
deleted_users_cache = set()

def main_handler(event, context):
    current_run_time = datetime.now(pytz.utc)
    delete_enabled = event.get('delete_enabled', 'false').lower() == 'true'
    
    # List all unconfirmed users, considering the last processed time from the cache
    unconfirmed_users = list_users(cognito_client, cognito_user_pool_id, aged_user_threshold_minutes, user_status, last_processed_time_cache)
    
    # Print the list of unconfirmed users
    print(f"{user_status} users older than {aged_user_threshold_minutes} minutes: {unconfirmed_users}")

    # Delete the unconfirmed users and collect the ones successfully deleted
    deleted_users = [user for user in unconfirmed_users if delete_users(cognito_client, cognito_user_pool_id, user, delete_enabled, deleted_users_cache)]

    if deleted_users:
        # Write the list of deleted users to S3
        write_deleted_users_to_s3(s3_client, deleted_users, s3_bucket_name, s3_key)
        # Send an email notification with the list of deleted users
        send_email_notification(sns_client, sns_topic_arn, deleted_users)
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

