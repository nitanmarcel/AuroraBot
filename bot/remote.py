from typing import List

import heroku3
from telegram.ext import CommandHandler, Filters

from bot import HEROK_API, dispatcher, update

heroku_conn = heroku3.from_key(HEROK_API)
app = heroku_conn.apps()['aurorabugsbunny']


def remote(bot, update, args: List[str]):
    if 'restart' in args:
        update.message.reply_text("Bot is restarting...")
        app.restart()
    elif 'log' in args:
        file = open('herokulog.txt', 'w')
        log = app.get_log(lines=20, timeout=1)
        file.write(log)
        file.close()
        bot.send_document(chat_id=update.message.chat_id,
                          document=open('herokulog.txt', 'rb'))
    elif 'log2' in args:
        bot.send_document(chat_id=update.message.chat_id,
                          document=open('logfile.txt', 'rb'))
    else:
        update.message.reply_text("""
                                  Did you mean:
                                  /remote restart - Restart the Bot
                                  /remote log - Sends you the latest app log [Use it in private]
                                  """)


def changes(bot, update):
    releases = app.releases(order_by='version', limit=3, sort='desc')
    for release in releases:
        print("{0} {1} {2} {3}".format(release.id,
                                       release.commit, release.user, release.description))


dispatcher.add_handler(CommandHandler(
    'remote', remote, Filters.user([463062143, 416195206, 504607607]), pass_args=True))
dispatcher.add_handler(CommandHandler('changes', changes))
