import json
import shutil
import tempfile
import unittest
import os
from book import Book
from book_catalog import BookCatalog



class TestBookCatalog(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.user_id = "test_user"

        # Модифицируем путь к файлу для использования временной директории
        BookCatalog._filename = os.path.join(self.test_dir, f'{self.user_id}_book_catalog.json')


    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_load_books_no_file(self):
        catalog = BookCatalog(self.user_id)
        self.assertEqual(catalog.get_all_books(), [])


    def test_load_books_with_file(self):
        test_data = [{
            "id": "9d59f8b5-b0e7-4aa9-a18b-8aa8e7ead5ce",
            "title": "Название1",
            "author": "Автор1",
            "tag": "тээээг",
            "is_read": True,
            "read_date": "2024-11-28 23:21:19.445979"
        }]

        test_user_id = "test_user"
        test_filename = f'../data/{test_user_id}_book_catalog.json'

        os.makedirs(os.path.dirname(test_filename), exist_ok=True)

        with open(test_filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        try:
            catalog = BookCatalog(test_user_id)
            books = catalog.get_all_books()

            self.assertEqual(len(books), 1)
            book = books[0]
            self.assertEqual(book._id, "9d59f8b5-b0e7-4aa9-a18b-8aa8e7ead5ce")
            self.assertEqual(book._title, "Название1")
            self.assertEqual(book._author, "Автор1")
            self.assertEqual(book._tag, "тээээг")
            self.assertTrue(book._is_read)
            self.assertEqual(book._read_date, "2024-11-28 23:21:19.445979")

        finally:
            if os.path.exists(test_filename):
                os.remove(test_filename)


    # инт
    def test_add_book(self):
        catalog = BookCatalog(self.user_id, os.path.join(self.test_dir, f'{self.user_id}_book_catalog.json'))

        book = Book("title1", "auth1", "tag1")

        catalog.add_book(book)

        all_books = catalog.get_all_books()
        self.assertEqual(len(all_books), 1)

        added_book = all_books[0]
        self.assertEqual(added_book._title, "title1")
        self.assertEqual(added_book._author, "auth1")
        self.assertEqual(added_book._tag, "tag1")

        expected_filename = os.path.join(self.test_dir, f'{self.user_id}_book_catalog.json')
        self.assertTrue(os.path.exists(expected_filename))

        new_catalog = BookCatalog(self.user_id, expected_filename)
        reloaded_books = new_catalog.get_all_books()
        self.assertEqual(len(reloaded_books), 1)

        reloaded_book = reloaded_books[0]
        self.assertEqual(reloaded_book._title, "title1")
        self.assertEqual(reloaded_book._author, "auth1")
        self.assertEqual(reloaded_book._tag, "tag1")
    

    # инт
    def test_save_books(self):
        catalog = BookCatalog(self.user_id, os.path.join(self.test_dir, f'{self.user_id}_book_catalog.json'))
    
        # Добавляем несколько книг
        book1 = Book("title1", "auth1", "tag1")
        book2 = Book("title2", "auth2", "tag2")
        catalog.add_book(book1)
        catalog.add_book(book2)
    
        # Проверяем файл
        with open(os.path.join(self.test_dir, f'{self.user_id}_book_catalog.json'), 'r', encoding='utf-8') as f:
            saved_books = json.load(f)
    
        self.assertEqual(len(saved_books), 2)
        self.assertEqual(saved_books[0]['title'], "title1")
        self.assertEqual(saved_books[1]['title'], "title2")

        
        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')


    # инт
    def test_get_unread_books(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book1 = Book("title1", "auth1", "tag1")
        book2 = Book("title2", "auth2", "tag2")
        book2.mark_as_read()
    
        catalog.add_book(book1)
        catalog.add_book(book2)
    
        unread_books = catalog.get_unread_books()
        self.assertEqual(len(unread_books), 1)
        self.assertEqual(unread_books[0]._title, "title1")

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')

    
    # инт
    def test_get_read_books(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book1 = Book("title1", "auth1", "tag1")
        book2 = Book("title2", "auth2", "tag2")
        book2.mark_as_read()
    
        catalog.add_book(book1)
        catalog.add_book(book2)
    
        read_books = catalog.get_read_books()
        self.assertEqual(len(read_books), 1)
        self.assertEqual(read_books[0]._title, "title2")

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')

    
    # инт
    def test_get_all_books(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book1 = Book("title1", "auth1", "tag1")
        book2 = Book("title2", "auth2", "tag2")
    
        catalog.add_book(book1)
        catalog.add_book(book2)
    
        all_books = catalog.get_all_books()
        self.assertEqual(len(all_books), 2)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    # инт
    def test_mark_book_as_read(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book = Book("title1", "auth1", "tag1")
        catalog.add_book(book)
    
        # Получаем ID книги
        book_id = book._id
    
        # Отмечаем книгу как прочитанную
        result = catalog.mark_book_as_read(book_id)
    
        self.assertTrue(result)
    
        # Проверяем, что книга помечена как прочитанная
        updated_book = catalog.get_book_by_id(book_id)
        self.assertTrue(updated_book._is_read)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    def test_mark_book_as_read_invalid(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        result = catalog.mark_book_as_read("invalid_id")
    
        self.assertFalse(result)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    # инт
    def test_remove_book(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book = Book("title1", "auth1", "tag1")
        catalog.add_book(book)
    
        # Получаем ID книги
        book_id = book._id
    
        # Удаляем книгу
        result = catalog.remove_book(book_id)
    
        self.assertTrue(result)
        self.assertEqual(len(catalog.get_all_books()), 0)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    def test_remove_book_invalid(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        result = catalog.remove_book("invalid_id")
    
        self.assertFalse(result)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    # инт
    def test_get_book_by_id(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        book = Book("title1", "auth1", "tag1")
        catalog.add_book(book)
    
        # Получаем книгу по ID
        found_book = catalog.get_book_by_id(book._id)
    
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book._title, "title1")

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')
    

    def test_get_book_by_id_invalid(self):
        catalog = BookCatalog(self.user_id, f'{self.user_id}_book_catalog.json')
    
        found_book = catalog.get_book_by_id("invalid_id")
    
        self.assertIsNone(found_book)

        if os.path.exists(f'{self.user_id}_book_catalog.json'):
            os.remove(f'{self.user_id}_book_catalog.json')


if __name__ == '__main__':
    unittest.main()