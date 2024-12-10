import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.book_catalog import BookCatalog, Book


class BookTelegramBot:
    def __init__(self, token):
        self._token = token
        self._user_catalogs = {}
        self._updater = Updater(token, use_context=True)
        self._setup_handlers()


    def _get_user_catalog(self, user_id):
        if user_id not in self._user_catalogs:
            self._user_catalogs[user_id] = BookCatalog(user_id)
        return self._user_catalogs[user_id]


    def _setup_handlers(self):
        dispatcher = self._updater.dispatcher
        
        add_book_handler = ConversationHandler(
            entry_points=[CommandHandler('add', self.start_add_book)],
            states={
                1: [MessageHandler(filters.Filters.text & ~filters.Filters.command, self.get_book_title)],
                2: [MessageHandler(filters.Filters.text & ~filters.Filters.command, self.get_book_author)],
                3: [MessageHandler(filters.Filters.text & ~filters.Filters.command, self.get_book_tag)]
            },
            fallbacks=[]
        )

        dispatcher.add_handler(add_book_handler)
        dispatcher.add_handler(CommandHandler('start', self.start_command))
        dispatcher.add_handler(CommandHandler('book_list', self.show_book_list))
        dispatcher.add_handler(CommandHandler('done_books', self.show_read_books))
        dispatcher.add_handler(CallbackQueryHandler(self.book_action_handler, pattern='^(?!back_button_clicked).*'))
        dispatcher.add_handler(CallbackQueryHandler(self.back_button_clicked, pattern='back_button_clicked'))


    def start_command(self, update, context):
        update.message.reply_text("Добро пожаловать в каталог книг!\n\n/add - добавить книгу в список книг \n/book_list - вывести список книг \n/done_books - вывести список прочитанных книг")


    def start_add_book(self, update, context):
        update.message.reply_text("Введите название книги:")
        return 1


    def get_book_title(self, update, context):
        context.user_data['book_title'] = update.message.text
        update.message.reply_text("Введите автора книги:")
        return 2


    def get_book_author(self, update, context):
        context.user_data['book_author'] = update.message.text
        update.message.reply_text("Введите тэг (пометку) для книги:")
        return 3


    def get_book_tag(self, update, context):
        user_id = update.effective_user.id
        catalog = self._get_user_catalog(user_id)
        
        try:
            book = Book(
                context.user_data['book_title'], 
                context.user_data['book_author'], 
                update.message.text
            )
            catalog.add_book(book)
            update.message.reply_text("Книга успешно добавлена в каталог!")
        except Exception as e:
            print(e)
            update.message.reply_text("Ошибка при добавлении книги.")
        
        return ConversationHandler.END


    def show_book_list(self, update, context):
        user_id = update.effective_user.id
        catalog = self._get_user_catalog(user_id)

        unread_books = catalog.get_unread_books()
        read_books = catalog.get_read_books()
        books = catalog.get_all_books()
        
        if not books:
            update.message.reply_text("Список книг пуст.")
            return

        keyboard = []

        for book in books:
            if book in unread_books:
                button_text =  f"{book._title} - {book._author}"                
            elif book in read_books:
                button_text =  f"✅ {book._title} - {book._author}"

            keyboard.append([
                    InlineKeyboardButton(
                        text=button_text, 
                        callback_data=f"book_{book._id}"
                    )
                ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message is None:
            context.bot.send_message(chat_id=user_id, text="Выберите книгу:", reply_markup=reply_markup)
        else:
            update.message.reply_text("Выберите книгу:", reply_markup=reply_markup)


    def book_action_handler(self, update, context):
        query = update.callback_query
        user_id = update.effective_user.id
        catalog = self._get_user_catalog(user_id)
        
        action, book_id = query.data.split('_')
        book = catalog.get_book_by_id(book_id)

        if not book:
            query.edit_message_text("Книга не найдена.")
            return

        query.answer()
        if action == 'book':
            if book.is_read():
                keyboard = [
                    [InlineKeyboardButton("Удалить книгу", callback_data=f"remove_{book_id}")],
                    [InlineKeyboardButton("Назад", callback_data="back_button_clicked")]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("Удалить книгу", callback_data=f"remove_{book_id}")],
                    [InlineKeyboardButton("Отметить прочитанной", callback_data=f"read_{book_id}")],
                    [InlineKeyboardButton("Назад", callback_data="back_button_clicked")]
                ]
                
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text=book.get_details(), 
                reply_markup=reply_markup
            )
        elif action == 'remove':
            if catalog.remove_book(book_id):
                query.edit_message_text("Книга удалена из каталога.")
            else:
                query.edit_message_text("Не удалось удалить книгу из каталога.")
        elif action == 'read':
            if catalog.mark_book_as_read(book_id):
                query.edit_message_text("Книга отмечена как прочитанная.")
            else:
                query.edit_message_text("Не удалось отметить книгу как прочитанную.")


    def back_button_clicked(self, update, context):
        query = update.callback_query

        query.answer()
        self.show_book_list(update, context)



    def show_read_books(self, update, context):
        user_id = update.effective_user.id
        catalog = self._get_user_catalog(user_id)
        read_books = catalog.get_read_books()
        
        if not read_books:
            update.message.reply_text("Нет прочитанных книг.")
            return

        response = "Прочитанные книги:\n\n"
        for book in read_books:
            response += (
                f"Название: {book._title}\n"
                f"Автор: {book._author}\n"
                f"Дата прочтения: {book._read_date}\n\n"
            )
        update.message.reply_text(response)


    def run(self):
        self._updater.start_polling()
        self._updater.idle()
