import unittest
from unittest.mock import MagicMock, Mock, patch
from telegram.ext import Updater
from bot import BookTelegramBot, ConversationHandler
from book_catalog import BookCatalog
from config import BOT_TOKEN


class TestBookTelegramBot(unittest.TestCase):
    def setUp(self):
        self.bot_token = BOT_TOKEN
        self.bot = BookTelegramBot(self.bot_token)


    def test_bot_initialization(self):
        self.assertEqual(self.bot._token, self.bot_token)
        self.assertIsInstance(self.bot._updater, Updater)
        self.assertTrue(hasattr(self.bot, '_user_catalogs'))


    def test_get_user_catalog(self):
        user_id = 12345
        catalog1 = self.bot._get_user_catalog(user_id)
        catalog2 = self.bot._get_user_catalog(user_id)
        
        self.assertIs(catalog1, catalog2)
        self.assertIsInstance(catalog1, BookCatalog)


    def test_setup_handlers(self):
        mock_dispatcher = Mock()
        self.bot._updater.dispatcher = mock_dispatcher

        self.bot._setup_handlers()
        self.assertEqual(mock_dispatcher.add_handler.call_count, 6)
        
        expected_handlers = [
            'ConversationHandler',
            'CommandHandler',  # start
            'CommandHandler',  # book_list
            'CommandHandler',  # done_books
            'CallbackQueryHandler',  # book action
            'CallbackQueryHandler'  # back button
        ]
        
        handler_names = [
            call[0][0].__class__.__name__ 
            for call in mock_dispatcher.add_handler.call_args_list
        ]
        
        for name in expected_handlers:
            self.assertIn(name, handler_names)


    # ат
    def test_start_command(self):
        mock_update = Mock()
        mock_context = Mock()
        
        self.bot.start_command(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_once_with(
            "Добро пожаловать в каталог книг!\n\n/add - добавить книгу в список книг \n/book_list - вывести список книг \n/done_books - вывести список прочитанных книг"
        )


    # ат
    @patch('book_catalog.BookCatalog')
    def test_get_book_tag_success(self, mock_book_catalog):
        mock_update = Mock()
        mock_context = Mock()
        
        mock_update.effective_user.id = 12345
        mock_update.message.text = 'test_tag'
        mock_context.user_data = {
            'book_title': 'Test Book',
            'book_author': 'Test Author'
        }
        
        self.bot._get_user_catalog = MagicMock(return_value=mock_book_catalog.return_value)
        
        result = self.bot.get_book_tag(mock_update, mock_context)
        
        mock_book_catalog.return_value.add_book.assert_called_once()
        mock_update.message.reply_text.assert_called_with("Книга успешно добавлена в каталог!")
        self.assertEqual(result, ConversationHandler.END)


    # аттестационный тест
    def test_get_book_tag_failure(self):
        mock_update = Mock()
        mock_context = Mock()
        
        mock_update.effective_user.id = 12345
        mock_update.message.text = 'test_tag'
        mock_context.user_data = {
            'book_title': 'Test Book',
            'book_author': 'Test Author'
        }
        
        self.bot._get_user_catalog = MagicMock()
        self.bot._get_user_catalog.return_value.add_book.side_effect = Exception("Test error")
        
        result = self.bot.get_book_tag(mock_update, mock_context)
        
        mock_update.message.reply_text.assert_called_with("Ошибка при добавлении книги.")
        self.assertEqual(result, ConversationHandler.END)


if __name__ == '__main__':
    unittest.main()
