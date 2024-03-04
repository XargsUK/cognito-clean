import logging

def send_email_notification(sns_client, topic_arn, deleted_users_info):
    """
    Sends an email notification with the list of deleted users via AWS SNS.

    :param sns_client: Boto3 SNS client
    :param topic_arn: The ARN of the SNS topic to publish the message to
    :param deleted_users_info: List of dictionaries containing user attributes
    """
    if not topic_arn:
        logging.info("Skipping SNS notification as topic has not been configured...")
        return
    if not sns_client:
        raise ValueError("error: sns_client not initialised")
    if not deleted_users_info:
        logging.info("No users deleted, skipping SNS notification...")
        return
    
    # Format the message with all user information
    message_lines = ["Deleted Users:"]
    for user in deleted_users_info:
        user_info = "\n".join([f"{attr['Name']}: {attr['Value']}" for attr in user['Attributes']])
        message_lines.append(f"Username: {user['Username']}\n{user_info}\n")
    message = "\n".join(message_lines)

    # Sending the message
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Notification of Deleted Users'
        )
        logging.info(f"Message sent to SNS topic {topic_arn}. Message ID: {response['MessageId']}")
    except Exception as e:
        logging.error(f"Failed to send notification due to an error: {e}")
