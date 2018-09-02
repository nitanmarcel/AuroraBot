import logging

from telegram import ParseMode
from telegram.ext import CommandHandler

from bot import (PORT, TOKEN, URL, bugs, dispatcher, misc, remote, suggestions,
                 update)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Up and running")


def help(bot, update):
    REPLY = """
    ```
    All users:
    /bug <bug> or (reply to message) - saves the bug on our db(if is a text message) or in our channel(if is a document)
    /suggestion - same as above but with suggestions
    /bugs - sends a txt file with the bugs in the database
    /suggestions - same as above but for suggestions
    /commits - get the latest 4 Aurora commits from GitLab
    \nSpecial users:
    \delb <id> - deletes the bug which id was specified [works with multiple ids too]
    \dels <id> - deletes the suggestion which id was specified [works with multiple ids too]
    !<id> - Get a suggestion or bug mathing the inserted id
    ```

    """
    bot.send_message(chat_id=update.message.chat_id,
                     text=REPLY, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))

    update.start_polling()
