from typing import List
from uuid import uuid4

from telegram import Bot, ChatAction, MessageEntity, ParseMode, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, RegexHandler
from telegram.ext.dispatcher import run_async

import bot.sql.suggestion_sql as sql
from bot import dispatcher, update
from bot.sql.bugs_sql import get_bug_id


def suggestion(bot, update, args: List[str]):
    message = update.effective_message
    if len(args) == 0 and not message.reply_to_message:
        message.reply_text("I don't see what suggestion you want to tell us")
    elif len(args) == 0 and message.reply_to_message:
        try:
            id = uuid4().hex[:8]
            sql.add_suggestion(id, message.reply_to_message.text)
            message.reply_text(
                "Your suggestion has been saved. Suggestion id is: " + id)
        except Exception:
            bot.send_message(chat_id='@secretchatbunny09090120', text="*Suggestion from* '{}''".format(
                message.reply_to_message.from_user.username), parse_mode=ParseMode.MARKDOWN)
            bot.forward_message(
                chat_id='@secretchatbunny09090120', from_chat_id=update.message.chat_id, message_id=message.reply_to_message.message_id)
            message.reply_text(
                "Your suggestion has been saved to the channel. There will be no id assigned")
    elif len(args) != 0 and not message.reply_to_message:
        id = uuid4().hex[:8]
        sql.add_suggestion(id, ' '.join(args))
        message.reply_text(
            "Your suggestion has been saved. Suggestion id is: *{}*".format(id), parse_mode=ParseMode.MARKDOWN)


def get(bot, update):
    file = open('suggestions.txt', 'w')
    for s in sql.get_suggestions():
        message = update.effective_message
        ROWS_TXT = "{} | {}".format(s.id, s.suggestion)

        file.write("\n%s\n" % ROWS_TXT)
        print(ROWS_TXT)
    try:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        file.close()
        bot.send_document(chat_id=update.message.chat_id,
                          document=open('suggestions.txt', 'rb'))
    except Exception:
        message.reply_text("There are no suggestions given so far")


def rm(bot, update, args: List[str]):
    message = update.effective_message
    remove = [sql.rem_suggestions(i) for i in args]
    message.reply_text("Suggestion(s) has been deleted")


dispatcher.add_handler(CommandHandler(
    "suggestion", suggestion, Filters.chat(-1001361570927), pass_args=True))

dispatcher.add_handler(CommandHandler('suggestions', get))

dispatcher.add_handler(CommandHandler('dels', rm, Filters.user(
    [463062143, 416195206, 504607607]), pass_args=True))
