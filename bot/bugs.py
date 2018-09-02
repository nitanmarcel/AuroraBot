from typing import List
from uuid import uuid4

from telegram import ChatAction, ParseMode
from telegram.ext import CommandHandler, Filters

import bot.sql.bugs_sql as sql
from bot import dispatcher, update


def bug(bot, update, args: List[str]):
    message = update.effective_message
    if len(args) == 0 and not message.reply_to_message:
        message.reply_text("I don't see what bug you want to report")
    elif len(args) == 0 and message.reply_to_message:
        try:
            id = uuid4().hex[:8]
            sql.add_bug(id, message.reply_to_message.text)
            message.reply_text(
                "Your bug has been saved. Bug id is: " + id)
        except Exception:
            bot.send_message(chat_id='@secretchatbunny09090120', text="**Bug reported by {}".format(
                message.reply_to_message.from_user.username), parse_mode=ParseMode.MARKDOWN)
            bot.forward_message(
                chat_id='@secretchatbunny09090120', from_chat_id=update.message.chat_id, message_id=message.reply_to_message.message_id)
            message.reply_text(
                "Your bug has been saved to the channel. There will be no id assigned")
    elif len(args) != 0 and not message.reply_to_message:
        id = uuid4().hex[:8]
        sql.add_bug(id, ' '.join(args))
        message.reply_text(
            "Your bug has been saved. The bugs id is: *{}*".format(id), parse_mode=ParseMode.MARKDOWN)


def get(bot, update):
    message = update.effective_message
    file = open('bugs.txt', 'w')
    for s in sql.get_bugs():
        ROWS_TXT = "{} | {}".format(s.id, s.bug)

        file.write("\n%s\n" % ROWS_TXT)
        print(ROWS_TXT)

    try:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        file.close()
        bot.send_document(chat_id=update.message.chat_id,
                          document=open('bugs.txt', 'rb'))
    except Exception:
        message.reply_text("There are no bugs reported so far")


def rm(bot, update, args: List[str]):
    message = update.effective_message
    remove = [sql.rem_bugs(i) for i in args]
    message.reply_text("Bug(s) has been deleted")


dispatcher.add_handler(CommandHandler(
    "bug", bug, Filters.chat(-1001361570927), pass_args=True))

dispatcher.add_handler(CommandHandler('bugs', get))

dispatcher.add_handler(CommandHandler('delb', rm, Filters.user(
    [463062143, 416195206, 504607607]), pass_args=True))
