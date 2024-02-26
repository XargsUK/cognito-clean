def send_email_notification(sns_client, topic_arn, deleted_users):
    """
    Sends an email notification with the list of deleted users via AWS SNS.

    :param sns_client: Boto3 SNS client
    :param topic_arn: The ARN of the SNS topic to publish the message to
    :param deleted_users: List of usernames that were deleted
    """
    if not topic_arn:
        print("Skipping SNS notification as topic has not been configured...")
        return
    if not sns_client:
        raise ValueError("ERROR: sns_client not initialised")
    if not deleted_users:
        print("No users deleted, skipping SNS notification...")
        return
    
    # Creating the message
    message = "Deleted Users:\n" + "\n".join(deleted_users)

    # Sending the message
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Notification of Deleted Users'
        )
        print(f"Message sent to SNS topic {topic_arn}. Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send notification due to an error: {e}")