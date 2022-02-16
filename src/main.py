#a simple python bot that will send random contents
#to its users

#ver 0.2.0

import logging
import threading
import hashlib
import queue as queues
import sqlite3 as db
import os.path as path
import botcommands as commands

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, InlineQueryHandler
from const import *
from utils import *
from config import *


DB_READER: db.Connection = None
DB_WRITER: db.Connection = None
QUEUE = queues.Queue()

# logging config 
logging.basicConfig(filename=PATH_LOG, filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)

def queue_handler():
    global DB_WRITER
    DB_WRITER = db.connect(DB_PATH, check_same_thread=False)

    while True:
        elem = QUEUE.get()
        if elem['type'] == 'word':
            store_db_word(DB_WRITER, elem['value'])
        elif elem['type'] == 'sticker':
            store_db_sticker(DB_WRITER, elem['uid'], elem['tid'])
        elif elem['type'] == 'photo':
            store_db_photo(DB_WRITER, elem['uid'], elem['tid'])
        elif elem['type'] == 'music':
            store_db_music(DB_WRITER, elem['uid'], elem['tid'])


def store_db_word(connection: db.Connection, word: str):
    f = hashlib.sha256()
    f.update(word.encode())
    try:
        connection.execute(INSERT_WORD_QUERY, (f.hexdigest(), word))
        connection.commit()
        logging.info(f"Added word to db ({word})")
    except Exception as e:
        logging.error(f"Failed to add word: {e}")
    

def store_db_sticker(connection: db.Connection, uid: str, tid: str):
    try:
        connection.execute(INSERT_STICKER_QUERY, (uid, tid))
        connection.commit()
        logging.info(f"Added sticker to db ({uid}, {tid})")
    except Exception as e:
        logging.error(f"Failed to add sticker: {e}")
    

def store_db_photo(connection, uid, tid):
    try:
        connection.execute(INSERT_PHOTO_QUERY, (uid, tid))
        connection.commit()
        logging.info(f"Added photo to db ({uid}, {tid})")
    except Exception as e:
        logging.error(f"Failed to add photo: {e}")


def store_db_music(connection, uid, tid):
    try:
        connection.execute(INSERT_MUSIC_QUERY, (uid, tid))
        connection.commit()
        logging.info(f"Added song to db ({uid}, {tid})")
    except Exception as e:
        logging.error(f"Failed to add song: {e}")


def setup():
    """setup things: create looper thread for queue and db connection"""
    global DB_READER 
    global QUEUE

    if not path.isfile(DB_PATH):
        DB_READER = create_database()
    else:
        DB_READER = db.connect(DB_PATH, check_same_thread=False)

    # add words in a thread safe way
    threading.Thread(target=queue_handler, daemon=True).start()

    # setup command handler
    commands.init(DB_READER, QUEUE)


def create_database() -> db.Connection:
    logging.info('Database not existing... creating new')

    con = db.connect(DB_PATH, check_same_thread=False)
    con.execute(CREATE_WORD_TABLE_QUERY)
    con.execute(CREATE_STICKER_TABLE_QUERY)
    con.execute(CREATE_IMAGES_TABLE_QUERY)
    con.execute(CREATE_MUSIC_TABLE_QUERY)
    con.commit()
    return con


def main():

    updater = Updater(TELEGRAM_BOT_TOKEN, use_context= True)
    dispatcher = updater.dispatcher

    add_word_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_ADD_TEXT, commands.add_word)],
        states={STATE_ONE: [MessageHandler(Filters.text, commands.store_word)]
            },
        fallbacks=[]
    )

    add_sticker_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_ADD_STICKER, commands.add_sticker)],
        states={
            STATE_ADDSTICKER: [
                MessageHandler(Filters.sticker, commands.store_sticker)
                ]
            },
        fallbacks=[CommandHandler(COMMAND_END, commands.stop_conversation)]
        )

    add_photo_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_ADD_PHOTO, commands.add_photo)],
        states={
            STATE_ADDPHOTO: [
                MessageHandler(Filters.photo, commands.store_photo)
                ]
            },
        fallbacks=[CommandHandler(COMMAND_END, commands.stop_conversation)]
    )

    add_music_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_ADD_AUDIO, commands.add_music)],
        states={
            STATE_ADDMUSIC: [
                MessageHandler(Filters.audio, commands.store_music)
                ]
            },
        fallbacks=[CommandHandler(COMMAND_END, commands.stop_conversation)]
    )

    dispatcher.add_handler(add_word_handler)
    dispatcher.add_handler(add_sticker_handler)
    dispatcher.add_handler(add_photo_handler)
    dispatcher.add_handler(add_music_handler)
    dispatcher.add_handler(InlineQueryHandler(commands.inlinequery))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_TEXT, commands.send_text))
    dispatcher.add_handler(CommandHandler(COMMAND_START, commands.start_handler))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_STICKER, commands.send_sticker))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_PHOTO, commands.send_photo))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_AUDIO, commands.send_music))
    dispatcher.add_handler(MessageHandler(Filters.text, commands.send_random_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, commands.direct_store_photo))
    
    logging.info('Telegram Random BOT started')
    updater.start_polling()
    updater.idle()



if __name__=='__main__':
    setup()
    main()
    if DB_READER is not None: DB_READER.close()
    if DB_WRITER is not None: DB_WRITER.close()