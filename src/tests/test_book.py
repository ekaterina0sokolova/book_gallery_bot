import unittest
import datetime
from book import Book


class TestBook(unittest.TestCase):
    def test_create_book(self):
        try:
            book = Book("title1", "auth1", "tag1")
            self.assertIsNotNone(book)
        except ValueError:
            self.fail("Не удалось создать книгу с корректными данными")

    def test_create_book_with_blank_name(self):
        with self.assertRaises(ValueError) as context:
            Book("", "auth1", "tag1")
        
        self.assertEqual(
            str(context.exception), 
            "Название книги не может быть пустым."
        )

    def test_create_book_with_blank_author(self):
        with self.assertRaises(ValueError) as context:
            Book("title1", "", "tag1")
        
        self.assertEqual(
            str(context.exception), 
            "Автор книги не может быть пустым значением."
        )

    def test_create_book_with_blank_tag(self):
        with self.assertRaises(ValueError) as context:
            Book("title1", "auth1", "")
        
        self.assertEqual(
            str(context.exception), 
            "Тэг книги не может быть пустым."
        )

    def test_get_details(self):
        book = Book("title1", "auth1", "tag1")
        expected_details = "Название: title1\nАвтор: auth1\nТег: tag1"
        self.assertEqual(book.get_details(), expected_details)

    def test_mark_as_read(self):
        book = Book("title1", "auth1", "tag1")
        book.mark_as_read()
        self.assertTrue(book.is_read())

    def test_set_time_stamp(self):
        book = Book("title1", "auth1", "tag1")
        book.mark_as_read()
        self.assertIsNotNone(book._read_date)

    def test_is_read(self):
        book = Book("title1", "auth1", "tag1")
        self.assertFalse(book.is_read())

if __name__ == '__main__':
    unittest.main()
