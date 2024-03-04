import unittest
from unittest.mock import Mock, patch
from cognito_clean.notification_service import send_email_notification
import logging

logging.basicConfig(level=logging.INFO)
TEST_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:MyTopic"

class TestSendEmailNotification(unittest.TestCase):
    def test_send_email_notification_no_topic_arn(self):
        sns_client_mock = Mock()
        with self.assertLogs() as log:
            send_email_notification(sns_client_mock, "", [])
        self.assertIn("Skipping SNS notification as topic has not been configured...", log.output[0])

    def test_send_email_notification_no_sns_client(self):
        with self.assertRaises(ValueError):
            send_email_notification(None, TEST_TOPIC_ARN, [])

    def test_send_email_notification_no_deleted_users_info(self):
        sns_client_mock = Mock()
        with self.assertLogs() as log:
            send_email_notification(sns_client_mock, TEST_TOPIC_ARN, [])
        self.assertIn("No users deleted, skipping SNS notification...", log.output[0])

    def test_send_email_notification_success(self):
        """
        Test that the function successfully sends a message and prints the correct log message when provided with valid parameters.
        """
        sns_client_mock = Mock()
        topic_arn = "arn:aws:sns:us-east-1:123456789012:MyTopic"
        deleted_users_info = [{"Username": "john_doe", "Attributes": [{"Name": "Email", "Value": "john@example.com"}]}]

        # Configure the mock's `publish` method to return a specific value
        sns_client_mock.publish.return_value = {"MessageId": "12345"}

        with self.assertLogs() as log:
            send_email_notification(sns_client_mock, topic_arn, deleted_users_info)

        # Assert that the `publish` method was called once with the expected arguments
        sns_client_mock.publish.assert_called_once_with(
            TopicArn=topic_arn,
            Message=unittest.mock.ANY,
            Subject='Notification of Deleted Users'
        )
        # Assert that the expected log message is in the output
        self.assertIn("Message sent to SNS topic arn:aws:sns:us-east-1:123456789012:MyTopic. Message ID: 12345", log.output[0])


    def test_send_email_notification_failure(self):
        sns_client_mock = Mock()
        sns_client_mock.publish.side_effect = Exception("AWS SNS Error")
        topic_arn = "arn:aws:sns:us-east-1:123456789012:MyTopic"
        deleted_users_info = [{"Username": "john_doe", "Attributes": [{"Name": "Email", "Value": "john@example.com"}]}]
        
        with self.assertLogs() as log:
            send_email_notification(sns_client_mock, topic_arn, deleted_users_info)
        
        self.assertIn("Failed to send notification due to an error: AWS SNS Error", log.output[0])

if __name__ == '__main__':
    unittest.main()
