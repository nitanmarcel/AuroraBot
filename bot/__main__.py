import logging

from telegram import ParseMode
from telegram.ext import CommandHandler, Filters, MessageHandler

from bot import BLACKLIST, PORT, TOKEN, URL, WHITELIST, dispatcher, update
from bot.modules import *

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


# Whitelist function starts here:
#
#     Set a channel id to WHITELIST so it will allow the bot to be added only on those channels
#     Set a channel id to BLACKLIST so it will allow not allow users to add the bot to those channels
#     If there are channels ids in both WHITELIST and BLACKLIST only the BLACKLISTs will be taken in considerations
#     Use export or heroku config:add (If you use heroku). config.py file will come soon.


def whitelist_empty():
    if len(WHITELIST) == 0:
        return True
    else:
        return False


def blacklist_empty():
    if len(BLACKLIST) == 0:
        return True
    else:
        return False


def is_chat_allowed(bot, update):
    if len(WHITELIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id not in WHITELIST_CHATS:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Unallowed chat! Leaving...')
            try:
                bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(BLACKLIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BLACKLIST_CHATS:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Unallowed chat! Leaving...')
            try:
                bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    if len(WHITELIST_CHATS) != 0 and len(BLACKLIST_CHATS) != 0:
        chat_id = update.effective_message.chat_id
        if chat_id in BLACKLIST_CHATS:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Unallowed chat, leaving')
            try:
                bot.leave_chat(chat_id)
            finally:
                raise DispatcherHandlerStop
    else:
        pass


if __name__ == '__main__':
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(
        Filters.group, is_chat_allowed))
    update.start_polling()
