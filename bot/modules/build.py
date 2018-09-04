import os
import re
import shutil
from datetime import datetime

from telegram import ChatAction, File
from telegram.ext import Filters, MessageHandler

from bot import dispatcher, update


def update_binary(ver):

    with open("magisk/META-INF/com/google/android/update-binary", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        get_date = datetime.today().strftime('%d-%m-%Y')
        replace_placeholder = re.sub(
            "placeholder", 'get_ver="{}"\nget_date="{}"'.format(ver, get_date), content)
        f.write(replace_placeholder)


def add_to_zip():
    shutil.copy('/app/AuroraStore.apk',
                '/tmp/aurora/system/priv-app/AuroraStore')
    os.remove('/tmp/aurora/system/priv-app/AuroraStore/placeholder')
    shutil.make_archive(base_name='MinAurora-signed',
                        format='zip', root_dir='/tmp/aurora', base_dir='./')


def build(bot, update):
    message = update.effective_message
    doc = message.document
    if doc.file_name.startswith('Aurora') and doc.file_name.endswith('.apk'):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Detected a new Aurora build. Creating new Magisk module..')
        split = re.split(r'-|.apk', doc.file_name)
        version = '-'.join(split[-3:]) + 'BOT-BUILD'
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.UPLOAD_DOCUMENT)
        apk_id = doc.file_id
        get_apk = bot.get_file(apk_id)
        get_apk.download(
            'AuroraStore.apk')
        shutil.copytree('magisk/', '/tmp/aurora')
        update_binary(version)
        add_to_zip()
        bot.send_document(chat_id=update.message.chat_id,
                          document=open("MinAurora-signed.zip", "rb"))
        os.remove('MinAurora-signed.zip')
        os.remove('AuroraStore.apk')


dispatcher.add_handler(MessageHandler(
    Filters.document, build))
