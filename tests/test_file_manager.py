import unittest
from unittest.mock import Mock
from cognito_clean.file_manager import write_deleted_users_to_s3
import logging
import json

logging.basicConfig(level=logging.INFO)

class TestWriteDeletedUsersToS3(unittest.TestCase):

    def test_skip_writing_to_s3_due_to_missing_bucket_or_key(self):
        s3_client_mock = Mock()
        with self.assertLogs() as log:
            write_deleted_users_to_s3(s3_client_mock, [{"username": "user1"}], bucket_name=None, s3_key=None)
        self.assertIn("Skipping writing to S3 as either bucket_name or s3_key has not been set...", log.output[0])
        s3_client_mock.put_object.assert_not_called()

    def test_successful_writing_to_s3(self):
        s3_client_mock = Mock()
        deleted_users_info = [{"username": "user1"}]
        bucket_name = "test-bucket"
        s3_key = "deleted_users.json"

        with self.assertLogs() as log:
            write_deleted_users_to_s3(s3_client_mock, deleted_users_info, bucket_name, s3_key)
        
        s3_client_mock.put_object.assert_called_once_with(
            Bucket=bucket_name, Key=s3_key, Body=json.dumps(deleted_users_info, indent=2)
        )
        self.assertIn(f"Successfully wrote deleted users to {s3_key} in bucket {bucket_name}.", log.output[0])

    def test_failure_writing_to_s3(self):
        s3_client_mock = Mock()
        s3_client_mock.put_object.side_effect = Exception("S3 Error")
        deleted_users_info = [{"username": "user2"}]
        bucket_name = "test-bucket"
        s3_key = "deleted_users_fail.json"

        with self.assertLogs() as log:
            write_deleted_users_to_s3(s3_client_mock, deleted_users_info, bucket_name, s3_key)

        self.assertIn("Failed to write deleted users to S3: S3 Error", log.output[0])

if __name__ == '__main__':
    unittest.main()
