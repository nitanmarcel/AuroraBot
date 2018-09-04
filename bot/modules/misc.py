from gitlab import Gitlab
from telegram import ParseMode
from telegram.ext import CommandHandler, RegexHandler

import bot.sql.suggestion_sql as sql
from bot import dispatcher, update
from bot.sql.bugs_sql import count_bugs, get_bug_id


def commit(bot, update):
    gl = Gitlab('https://gitlab.com/')
    project = gl.projects.get('6922885')
    commits = project.commits.list(ref_name='master', as_list=True)
    last_commits = []
    for i in commits[:4]:
        last_commits.append(i.title)

    update.message.reply_text(
        "The latest 4 commits from [GitLab](https://gitlab.com/AuroraOSS/AuroraStore) are:\n\n *{}*".format('\n'.join(last_commits)), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def excl_get(bot, update):
    message = update.effective_message
    excl_word = message.text.split()[0]
    no_excl = excl_word[1:]
    suggestion = sql.get_suggestions_id(no_excl)
    bug = get_bug_id(no_excl)
    if suggestion:
        message.reply_text(
            'I found a suggestion with the id: `{}`\n\n*{}*'.format(no_excl, suggestion.suggestion), parse_mode=ParseMode.MARKDOWN)
    elif bug:
        message.reply_text(
            "I found a suggestion with the id: `{}`:\n\n*{}*".format(no_excl, bug.bug), parse_mode=ParseMode.MARKDOWN)
    else:
        message.reply_text(
            "There is no bug/suggestion matching the id {}".format(no_excl), ParseMode=ParseMode.MARKDOWN)


def stats(bot, update):
    bugs_in_db = count_bugs()
    suggs_in_db = sql.count_suggestions()
    admins_in_group = bot.get_chat_administrators(update.message.chat.id)
    admins_list = []
    message = update.effective_message
    for admins in admins_in_group:
        admins_list.append(admins.user.username)

    REPLY = """
    *Current stats:*
    *Bugs:* `{}`,
    *Suggestions:* `{}`,
    *The admins of this group are:* `{}`
    """.format(bugs_in_db, suggs_in_db, ', '.join(admins_list))
    message.reply_text(REPLY, parse_mode=ParseMode.MARKDOWN)


dispatcher.add_handler(CommandHandler('commits', commit))
dispatcher.add_handler(RegexHandler(r"^![^\s]+", excl_get))
dispatcher.add_handler(CommandHandler('stats', stats))
