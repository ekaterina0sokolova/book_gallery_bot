import unittest
from unittest.mock import MagicMock, Mock, patch
from telegram.ext import Updater
from src.bot import BookTelegramBot, ConversationHandler
from src.book_catalog import BookCatalog
from src.config import BOT_TOKEN


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


    # атjnkn
    @patch('src.book_catalog.BookCatalog')
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

    
    def test_book_action_book_invalid(self):
        bot = BookTelegramBot(self.bot_token)  
        mock_update = Mock()
        mock_context = Mock()
        mock_catalog = Mock()
        
        user_id = 12345
        mock_update.effective_user.id = user_id
        mock_update.callback_query = Mock()
        
        bot._get_user_catalog = Mock(return_value=mock_catalog)
        
        # Книга не найдена
        mock_update.callback_query.data = "book_nonexistent"
        mock_catalog.get_book_by_id.return_value = None
        
        bot.book_action_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_called_once_with("Книга не найдена.")
        

    def test_book_action_unread_book_success(self):
        bot = BookTelegramBot(self.bot_token)  
        mock_update = Mock()
        mock_context = Mock()
        mock_catalog = Mock()
        
        user_id = 12345
        mock_update.effective_user.id = user_id
        mock_update.callback_query = Mock()
        
        bot._get_user_catalog = Mock(return_value=mock_catalog)
        
        # Книга найдена, не прочитана
        mock_book = Mock()
        mock_book.is_read.return_value = False
        mock_book.get_details.return_value = "Детали книги"
        mock_catalog.get_book_by_id.return_value = mock_book
        mock_update.callback_query.data = "book_123"
        
        bot.book_action_handler(mock_update, mock_context)
        
        # Check edit_message_text call
        mock_update.callback_query.edit_message_text.assert_called_once()
        call_args = mock_update.callback_query.edit_message_text.call_args[1]
        
        assert call_args['text'] == "Детали книги"
        
        # клавиатура
        reply_markup = call_args['reply_markup']
        keyboard_buttons = [button.text for row in reply_markup.inline_keyboard for button in row]
        assert "Удалить книгу" in keyboard_buttons
        assert "Отметить прочитанной" in keyboard_buttons
        assert "Назад" in keyboard_buttons

    
    def test_book_action_unread_book_invalid(self):
        bot = BookTelegramBot(self.bot_token)  
        mock_update = Mock()
        mock_context = Mock()
        mock_catalog = Mock()
        mock_book = Mock()
        
        user_id = 12345
        mock_update.effective_user.id = user_id
        mock_update.callback_query = Mock()
        
        bot._get_user_catalog = Mock(return_value=mock_catalog)
        
        # Книга найдена, прочитана
        mock_book.is_read.return_value = True
        mock_update.callback_query.data = "book_123"
        
        bot.book_action_handler(mock_update, mock_context)
        
        mock_update.callback_query.edit_message_text.assert_called_once()
        call_args = mock_update.callback_query.edit_message_text.call_args[1]
        
        # клавиатура
        reply_markup = call_args['reply_markup']
        keyboard_buttons = [button.text for row in reply_markup.inline_keyboard for button in row]
        assert "Удалить книгу" in keyboard_buttons
        assert "Отметить прочитанной" not in keyboard_buttons
        assert "Назад" in keyboard_buttons


    def test_book_action_remove_book(self):
        bot = BookTelegramBot(self.bot_token)  
        mock_update = Mock()
        mock_context = Mock()
        mock_catalog = Mock()
        
        bot._get_user_catalog = Mock(return_value=mock_catalog)
        
        user_id = 12345
        mock_update.effective_user.id = user_id
        mock_update.callback_query = Mock()

        mock_book = Mock()
        mock_catalog.get_book_by_id = Mock(return_value=mock_book)

        # Удаление книги
        mock_update.callback_query.data = "remove_123"
        mock_catalog.remove_book.return_value = True
        
        bot.book_action_handler(mock_update, mock_context)
        bot._get_user_catalog.assert_called_once_with(user_id)
        mock_catalog.get_book_by_id.assert_called_once_with("123")
        mock_catalog.remove_book.assert_called_once_with("123")
        mock_update.callback_query.edit_message_text.assert_called_once_with("Книга удалена из каталога.")
        
        
    def test_book_action_remove_book_invalid(self):
        bot = BookTelegramBot(self.bot_token)  
        mock_update = Mock()
        mock_context = Mock()
        mock_catalog = Mock()
        
        bot._get_user_catalog = Mock(return_value=mock_catalog)
        
        user_id = 12345
        mock_update.effective_user.id = user_id
        mock_update.callback_query = Mock()

        mock_book = Mock()
        mock_catalog.get_book_by_id = Mock(return_value=mock_book)

        # Удаление книги
        mock_update.callback_query.data = "remove_123"
        mock_catalog.remove_book.return_value = False
        
        bot.book_action_handler(mock_update, mock_context)
        bot._get_user_catalog.assert_called_once_with(user_id)
        mock_catalog.remove_book.assert_called_once_with("123")            


if __name__ == '__main__':
    unittest.main()
