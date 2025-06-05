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

---
```mermaid
graph TD
    A[Начало] --> B[Получение API-ключа пользователя: get_api_key(chat_id)]
    B --> C[Создание клиента OpenAI: create_openai_obj(api_key)]
    C --> D[Подключение к базе данных: connect_to_db()]
    D --> E[Получение текущего диалога: get_dialog(chat_id)]
    E --> F[Извлечение ID ассистента из диалога]
    F --> G[Вызов функции create_thread_and_run]
    G --> H{Проверка существования треда ассистента}
    H -->|Тред существует| I[Отправка сообщения в существующий тред]
    H -->|Тред отсутствует| J[Создание нового треда]
    J --> K[Обновление информации в базе данных]
    K --> L[Отправка сообщения пользователя: submit_message]
    I --> L
    L --> M[Создание сообщения в треде: client.beta.threads.messages.create]
    M --> N[Запуск потока обработки: client.beta.threads.runs.stream]
    N --> O[Обработка ответа в реальном времени: StreamEventHandler]
    O --> P[Сбор ответа по частям в result_text]
    P --> Q{Проверка на ошибки}
    Q -->|Ошибка 429| R[Возврат сообщения о недостатке токенов]
    Q -->|Другие ошибки| S[Логирование и обработка ошибки]
    Q -->|Нет ошибок| T[Формирование результата]
    S --> T
    R --> T
    T --> U[Возврат кортежа: (статус, текст ответа)]
    U --> V[Конец]

