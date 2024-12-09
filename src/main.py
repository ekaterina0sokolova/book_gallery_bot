from config import BOT_TOKEN
from bot import BookTelegramBot


def main():
    bot = BookTelegramBot(BOT_TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
