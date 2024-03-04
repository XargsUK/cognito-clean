import json

def write_deleted_users_to_s3(s3_client, deleted_users_info, bucket_name=None, s3_key=None):
    """
    Writes the list of deleted user objects to a file in an S3 bucket in JSON format. Skips writing if
    bucket_name or s3_key is not provided.

    :param s3_client: Boto3 S3 client
    :param deleted_users_info: List of dictionaries containing user attributes
    :param bucket_name: The name of the S3 bucket where the file will be stored, optional
    :param s3_key: The S3 key (file path within the bucket) for the file, optional
    """
    if not bucket_name or not s3_key:
        print("Skipping writing to S3 as either bucket_name or s3_key has not been set...")
        return

    # Convert the list of deleted user objects to a JSON string
    deleted_users_json = json.dumps(deleted_users_info, indent=2)

    try:
        # Proceed to write the JSON string to a file in S3
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=deleted_users_json)
        print(f"Successfully wrote deleted users to {s3_key} in bucket {bucket_name}.")
    except Exception as e:
        print(f"Failed to write deleted users to S3: {e}")
