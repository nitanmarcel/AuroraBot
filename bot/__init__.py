import glob
import os
from os.path import basename, dirname, isfile

from telegram.ext import Updater

TOKEN = os.environ.get('TOKEN', None)
update = Updater(TOKEN)
dispatcher = update.dispatcher

URL = os.environ.get('URL', "")
PORT = int(os.environ.get('PORT', 5000))

DB_URL = os.environ.get("DATABASE_URL", "")

HEROKU_API = os.environ.get("HERO_API", "")

WHITELIST = set(int(x) for x in os.environ.get("WHITELIST", "").split())

BLACKLIST = set(int(x) for x in os.environ.get("BLACKLIST", "").split())
