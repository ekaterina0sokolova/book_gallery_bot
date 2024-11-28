## Команды и возможности бота

* ```/start``` - запуск бота
* ```/add``` - добавить книгу в список книг
* ```/book_list``` - вывести список книг
  * Отметить книгу как прочитанную
  * Удалить книгу
* ```/done_books ``` - вывести список прочитанных книг


***
## Установка и запуск

Клонируем репозиторий
```
git clone https://github.com/ekaterina0sokolova/book_gallery_bot.git
cd book_gallery_bot
```

Создаем вирутальную среду
```
python -m venv venv
```
Активируем виртуальную среду
```
# для Linux или macOS:
source venv/bin/activate

# для Windows:
venv\Scripts\activate
```

Устанавливаем зависимости
```
pip install -r requirements.txt
```

Для работы программы Вам потребуется создать телеграм бота через [BotFather](https://t.me/botfather).

Создаем в папке scr файл .env и прописываем туда токен созданного телеграм бота:
```
# .env
BOT_TOKEN=YOUR_BOT_TOKEN
```

Запустить бота можно из корневой папки проекта (book_gallery_bot):
```
python src/main.py
```

***
## Запуск тестов
##### Запуск всех тестов
```
python -m unittest discover tests
```

##### Запуск тестов для конкретного класса
```
python -m unittest tests.test_book
python -m unittest tests.test_book_catalog
python -m unittest tests.test_bot
```

