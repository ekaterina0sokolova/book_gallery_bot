import unittest
import os
from src.book_catalog import Book, BookCatalog


class TestBookCatalog(unittest.TestCase):
    def setUp(self):
        self.user_id = 12345
        self.catalog = BookCatalog(self.user_id)
        self.test_filename = f'{self.user_id}_book_catalog.json'


    def tearDown(self):
        # Clean up test file after each test
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


    def test_add_book(self):
        book = Book("Title", "Author", "Genre")
        self.assertTrue(self.catalog.add_book(book))
        self.assertEqual(len(self.catalog._books), 1)


    def test_add_book_with_invalid_title(self):
        book = Book("", "Author", "Genre")
        self.assertFalse(self.catalog.add_book(book))
        self.assertEqual(len(self.catalog._books), 0)


    def test_get_unread_books(self):
        book1 = Book("Unread 1", "Author1", "Genre1")
        book2 = Book("Read Book", "Author2", "Genre2")
        book2.mark_as_read()

        self.catalog.add_book(book1)
        self.catalog.add_book(book2)

        unread_books = self.catalog.get_unread_books()
        self.assertEqual(len(unread_books), 1)
        self.assertEqual(unread_books[0]._title, "Unread 1")


    def test_get_read_books(self):
        book1 = Book("Unread Book", "Author1", "Genre1")
        book2 = Book("Read Book", "Author2", "Genre2")
        book2.mark_as_read()

        self.catalog.add_book(book1)
        self.catalog.add_book(book2)

        read_books = self.catalog.get_read_books()
        self.assertEqual(len(read_books), 1)
        self.assertEqual(read_books[0]._title, "Read Book")


    def test_mark_book_as_read(self):
        book = Book("Test Book", "Author", "Genre")
        self.catalog.add_book(book)
        
        # Mark the book as read by its ID
        self.assertTrue(self.catalog.mark_book_as_read(book._id))
        
        # Verify the book is now read
        updated_book = self.catalog.get_book_by_id(book._id)
        self.assertTrue(updated_book._is_read)


    def test_remove_book(self):
        book = Book("Test Book", "Author", "Genre")
        self.catalog.add_book(book)
        
        # Remove the book by its ID
        self.assertTrue(self.catalog.remove_book(book._id))
        self.assertEqual(len(self.catalog._books), 0)


    def test_get_book_by_id(self):
        book = Book("Test Book", "Author", "Genre")
        self.catalog.add_book(book)
        
        retrieved_book = self.catalog.get_book_by_id(book._id)
        self.assertIsNotNone(retrieved_book)
        self.assertEqual(retrieved_book._title, "Test Book")


if __name__ == '__main__':
    unittest.main()