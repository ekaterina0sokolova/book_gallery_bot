import datetime
import uuid

class Book:
    def __init__(self, title, author, tag):
        self._id = str(uuid.uuid4())
        self._title = title
        self._author = author
        self._tag = tag
        self._added_date = datetime.datetime.now()
        self._is_read = False
        self._read_date = None

        if not self._validate_title():
            raise ValueError("Название книги не может быть пустым.")
        
        if not self._validate_author():
            raise ValueError("Автор книги не может быть пустым значением.")
        
        if not self._validate_tag():
            raise ValueError("Тэг книги не может быть пустым.")


    def get_details(self):
        return (f"Название: {self._title}\n"
                f"Автор: {self._author}\n"
                f"Тег: {self._tag}")


    def mark_as_read(self):
        self._is_read = True
        self._read_date = datetime.datetime.now()


    def is_read(self):
        return self._is_read


    def _validate_title(self):
        return len(self._title) > 0
    

    def _validate_author(self):
        return len(self._author) > 0
    

    def _validate_tag(self):
        return len(self._tag) > 0
    