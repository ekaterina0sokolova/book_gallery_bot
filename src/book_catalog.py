import json
import os

from book import *

class BookCatalog:
    def __init__(self, user_id) -> None:
        self._user_id = user_id
        self._filename = f'../data/{user_id}_book_catalog.json'
        self._books = self._load_books()


    def _load_books(self) -> list:
        if not os.path.exists(self._filename):
            return []
        with open(self._filename, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
            books = []
            for book in book_data:
                new_book = Book(book['title'], book['author'], book['tag'])
                new_book._id = book.get('id', str(uuid.uuid4()))
                new_book._is_read = book.get('is_read', False)
                new_book._read_date = book.get('read_date')
                books.append(new_book)
            return books


    def add_book(self, book: Book) -> None:
        self._books.append(book)
        self._save_books()


    def _save_books(self) -> None:
        book_data = [
            {
                'id': book._id,
                'title': book._title, 
                'author': book._author, 
                'tag': book._tag,
                'is_read': book._is_read,
                'read_date': str(book._read_date) if book._read_date else None
            } for book in self._books
        ]
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=4)


    def get_unread_books(self) -> list:
        return [book for book in self._books if not book._is_read]


    def get_read_books(self)  -> list:
        return [book for book in self._books if book._is_read]
    
    
    def get_all_books(self)  -> list:
        return [book for book in self._books]
    

    def mark_book_as_read(self, book_id) -> bool:
        book = self.get_book_by_id(book_id)
        if book:
            book.mark_as_read()
            self._save_books()
            return True
        return False


    def remove_book(self, book_id) -> bool:
        book = self.get_book_by_id(book_id)
        if book:
            self._books.remove(book)
            self._save_books()
            return True
        return False


    def get_book_by_id(self, book_id):
        return next((book for book in self._books if book._id == book_id), None)
    