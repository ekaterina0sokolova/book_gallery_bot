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


    def get_details(self):
        return (f"Название: {self._title}\n"
                f"Автор: {self._author}\n"
                f"Тег: {self._tag}")


    def mark_as_read(self):
        self._is_read = True
        self._read_date = datetime.datetime.now()


    def _validate_title(self):
        return len(self._title) > 0
    