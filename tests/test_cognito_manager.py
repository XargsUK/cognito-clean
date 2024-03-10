import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import pytz
from cognito_clean.cognito_manager import list_users, delete_users, process_unconfirmed_users

class TestListUsers(unittest.TestCase):
    @patch('cognito_clean.cognito_manager.datetime')
    def test_list_users_filters_correctly(self, mock_datetime):
        # Setup mock datetime
        mock_now = datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock Cognito client
        cognito_client_mock = Mock()
        cognito_client_mock.get_paginator.return_value.paginate.return_value = [
            {'Users': [{'Username': 'user1', 'UserCreateDate': mock_now - timedelta(minutes=10)},
            {'Username': 'user2', 'UserCreateDate': mock_now - timedelta(hours=1)}]}
        ]

        # Call the function
        aged_users = list_users(cognito_client_mock, 'user_pool_id', 30, 'CONFIRMED', {})

        # Assertions
        self.assertEqual(len(aged_users), 1)
        self.assertEqual(aged_users[0]['Username'], 'user2')

if __name__ == '__main__':
    unittest.main()

class TestDeleteUsers(unittest.TestCase):
    def test_delete_users(self):
        cognito_client_mock = Mock()
        user = {'Username': 'test_user'}
        user_pool_id = 'user_pool_id'
        deleted_users_cache = set()

        # Case 1: Deletion enabled, user not in cache
        result = delete_users(cognito_client_mock, user_pool_id, user, True, deleted_users_cache)
        self.assertIsNotNone(result)
        self.assertIn('test_user', deleted_users_cache)

        # Case 2: User already deleted (in cache)
        result = delete_users(cognito_client_mock, user_pool_id, user, True, deleted_users_cache)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

class TestProcessUnconfirmedUsers(unittest.TestCase):
    @patch('cognito_clean.cognito_manager.delete_users')
    @patch('cognito_clean.cognito_manager.list_users')
    def test_process_unconfirmed_users(self, mock_list_users, mock_delete_users):
        # Setup mocks
        cognito_client_mock = Mock()
        mock_list_users.return_value = [{'Username': 'user1'}, {'Username': 'user2'}]
        mock_delete_users.side_effect = lambda client, pool_id, user, enabled, cache: user if enabled else None

        user_pool_id = 'user_pool_id'
        deleted_users_cache = set()

        # Invoke the processing function
        usernames, user_objects = process_unconfirmed_users(cognito_client_mock, user_pool_id, 30, 'CONFIRMED', True, {}, deleted_users_cache)

        # Assertions
        self.assertEqual(len(usernames), 2)
        self.assertEqual(len(user_objects), 2)
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)

if __name__ == '__main__':
    unittest.main()
