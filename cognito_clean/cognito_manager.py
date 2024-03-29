from datetime import datetime, timedelta
import pytz


def list_users(cognito_client, user_pool_id, age_in_minutes, user_statuses, last_run_cache):
    """
    List users from Cognito based on specified statuses and age, adjusted by the last processed time in cache.

    :param cognito_client: The Boto3 client for Cognito
    :param user_pool_id: The ID of the Cognito User Pool
    :param age_in_minutes: The age of the users in minutes to filter by
    :param user_statuses: Comma separated statuses of the users to filter by
    :param last_run_cache: A dictionary serving as cache to store the last run timestamp
    :return: A list of user objects with specified statuses older than 'age_in_minutes' or since last cache timestamp
    """
    try:
        # Ensure age_in_minutes is an integer
        age_in_minutes = int(age_in_minutes)
        
        # Attempt to get the last run time from cache
        last_run_time = last_run_cache.get(user_pool_id)

        # Calculate the cutoff time
        if last_run_time:
            cutoff_time = last_run_time
        else:
            # If not available in cache, calculate cutoff time based on age_in_minutes
            cutoff_time = datetime.now(pytz.utc) - timedelta(minutes=age_in_minutes)

        # Initialise the list to store the filtered user objects
        aged_user_objects = []

        # Split the user_statuses into a list
        statuses = user_statuses.split(',')

        # Paginate through the list_users response for each status
        for status in statuses:
            paginator = cognito_client.get_paginator('list_users')
            for page in paginator.paginate(UserPoolId=user_pool_id, Filter=f'cognito:user_status="{status}"'):
                for user in page['Users']:
                    user_creation_time = user['UserCreateDate']

                    # Ensure user_creation_time is timezone-aware and in UTC
                    if user_creation_time.tzinfo is None or user_creation_time.tzinfo.utcoffset(user_creation_time) is None:
                        user_creation_time = pytz.utc.localize(user_creation_time)

                    # Compare the user creation time with the cutoff time
                    if user_creation_time < cutoff_time:
                        aged_user_objects.append(user)  # Append the entire user object
        
        return aged_user_objects
    except Exception as e:
        print(f"Error listing users: {e}")
        return []


def delete_users(cognito_client, user_pool_id, user, delete_enabled, deleted_users_cache):
    """
    Deletes a single user from the Cognito user pool if delete_enabled is true.
    
    :param cognito_client: Boto3 Cognito client
    :param user_pool_id: String identifier of the Cognito user pool
    :param user: Dictionary containing user attributes
    :param delete_enabled: Boolean value to determine if the user should be deleted
    :param deleted_users_cache: Set to store usernames of deleted users
    :return: The user object if deletion was successful, otherwise None
    """
    username = user['Username']
    if delete_enabled:
        try:
            # Check if the user has already been deleted
            if username in deleted_users_cache:
                print(f"User {username} has already been deleted.")
                return None
            
            cognito_client.admin_delete_user(
                UserPoolId=user_pool_id,
                Username=username
            )
            
            # Update cache after successful deletion
            deleted_users_cache.add(username)
            return user  # Return the entire user object
        except Exception as e:
            print(f"Error deleting user {username}: {e}")
            return None
    else:
        print(f"Skipping deletion of user {username} as delete_enabled is not set to 'True'")
        return None


def process_unconfirmed_users(cognito_client, user_pool_id, age_in_minutes, user_statuses, delete_enabled, last_run_cache, deleted_users_cache):
    unconfirmed_users = list_users(cognito_client, user_pool_id, age_in_minutes, user_statuses, last_run_cache)
    deleted_usernames = []
    deleted_user_objects = []
    for user in unconfirmed_users:
        deleted_user = delete_users(cognito_client, user_pool_id, user, delete_enabled, deleted_users_cache)
        if deleted_user:
            deleted_usernames.append(user['Username'])
            deleted_user_objects.append(deleted_user)
    return deleted_usernames, deleted_user_objects
