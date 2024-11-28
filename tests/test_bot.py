import unittest

import unittest
from unittest.mock import patch
from src.bot import BookTelegramBot

class TestBookTelegramBot(unittest.TestCase):
    def setUp(self):
        self.bot_token = 'TEST_TOKEN'
        self.bot = BookTelegramBot(self.bot_token)

    @patch('telegram.ext.Updater')
    def test_bot_initialization(self, mock_updater):
        mock_updater.assert_called_once_with(token=self.bot_token, use_context=True)

    def test_get_user_catalog(self):
        user_id = 12345
        catalog1 = self.bot._get_user_catalog(user_id)
        catalog2 = self.bot._get_user_catalog(user_id)
        
        self.assertIs(catalog1, catalog2)

if __name__ == '__main__':
    unittest.main()