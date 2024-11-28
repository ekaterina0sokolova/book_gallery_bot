import unittest
import datetime
from src.book import Book


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Тест Название", "Тест Автор", "Тэг")


    def test_book_initialization(self):
        self.assertIsNotNone(self.book._id)
        self.assertEqual(self.book._title, "Тест Название")
        self.assertEqual(self.book._author, "Тест Автор")
        self.assertEqual(self.book._tag, "Тэг")
        self.assertFalse(self.book._is_read)
        self.assertIsNone(self.book._read_date)


    def test_get_details(self):
        details = self.book.get_details()
        self.assertIn("Тест Название", details)
        self.assertIn("Тест Автор", details)
        self.assertIn("Тэг", details)


    def test_mark_as_read(self):
        self.book.mark_as_read()
        self.assertTrue(self.book._is_read)
        self.assertIsNotNone(self.book._read_date)
        self.assertIsInstance(self.book._read_date, datetime.datetime)


    def test_validate_title(self):
        # Private method, accessing through a test case
        book_with_empty_title = Book("", "Тест Автор", "Тэг")
        self.assertFalse(book_with_empty_title._validate_title())
        
        book_with_valid_title = Book("Valid Title", "Тест Автор", "Тэг")
        self.assertTrue(book_with_valid_title._validate_title())


if __name__ == '__main__':
    unittest.main()
