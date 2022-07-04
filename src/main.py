#a simple python bot that will send random contents
#to its users

#ver 0.2.0

import logging, threading
from multiprocessing import connection
import queue as queues
from time import sleep
from matplotlib.pyplot import connect

import telegram
import botcommands as commands
import sqlite3 as db
import os.path as path

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, InlineQueryHandler
from const import *
from utils import *
from config import *
import random
import hashlib

db_reader: db.Connection = None
db_writer: db.Connection = None
queue = queues.Queue()

# logging config 
logging.basicConfig(filename=PATH_LOG, filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)

first_start= True

def message_scheduler_thread():
    first_start = True
    worker = db.connect(DB_PATH, check_same_thread=False)
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    handlers = [get_random_sticker, get_random_photo, get_random_word]
    logging.info("Message scheduler started")

    def send(type: int, chatid: int):
        if type == 0:
            msg = handlers[0](worker, 1)
            bot.sendSticker(chatid, msg[0])
        if type == 1:
            msg = handlers[1](worker, 1)
            bot.sendPhoto(chatid, msg[0])
        if type == 2:
            msg = handlers[2](worker, 1)
            bot.sendMessage(chatid, msg[0])

    while True:
        ids = worker.execute(GET_CHATID_QUERY).fetchall()
        for idt in ids:
            try:
                if first_start:
                    bot.sendMessage(idt[0], START_CHAT_MSG)
                else:
                    send(random.randint(0,2), idt[0])
            except Exception as e:
                logging.error(e)
            sleep(1)
        first_start = False
        #sleep(20)
        sleep(random.randint(4140,86400))



def queue_handler():
    global db_writer
    db_writer = db.connect(DB_PATH, check_same_thread=False)

    while True:
        elem = queue.get()
        if elem['type'] == 'word':
            store_db_word(db_writer, elem['value'])
        elif elem['type'] == 'sticker':
            store_db_sticker(db_writer, elem['uid'], elem['tid'])
        elif elem['type'] == 'photo':
            store_db_photo(db_writer, elem['uid'], elem['tid'])
        elif elem['type'] == 'music':
            store_db_music(db_writer, elem['uid'], elem['tid'])
        elif elem['type'] == 'enablerandomchat':
            store_for_random_messages(db_writer, elem['value'])
        elif elem['type'] == 'disablerandomchat':
            cancel_for_random_messages(db_writer, elem['value'])
        elif elem['type'] == 'gif':
            store_db_gif(db_writer, elem['uid'], elem['tid'])
        elif elem['type'] == 'customreply':
            store_custom_reply(db_writer, elem['value'])


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

def store_db_gif(connection, uid, tid):
    try:
        connection.execute(INSERT_GIF_QUERY, (uid, tid))
        connection.commit()
        logging.info(f"Added gif to db ({uid}, {tid})")
    except Exception as e:
        logging.error(f"Failed to add gif: {e}")


def store_custom_reply(connection, holder: CustomQueryDataHolder):
    try:
        connection.execute(INSERT_CUSTOM_REPLY_QUERY, (holder.query, holder.answer))
        connection.commit()
        logging.info(f"Added custom reply to db ({holder.query} -> {holder.answer})")
    except Exception as e:
        logging.error(f"Failed to add customreply: {e}")

def store_db_music(connection, uid, tid):
    try:
        connection.execute(INSERT_MUSIC_QUERY, (uid, tid))
        connection.commit()
        logging.info(f"Added song to db ({uid}, {tid})")
    except Exception as e:
        logging.error(f"Failed to add song: {e}")

def store_for_random_messages(connection: db.Connection, chatid: int):
    try:
        connection.execute(INSERT_CHATID_QUERY, (chatid,))
        connection.commit()
        logging.info(f"Added chat id to random message queue({chatid})")
    except Exception as e:
        logging.info(f"Failed to add chatid({e})")

def cancel_for_random_messages(connection: db.Connection, chatid: int):
    try:
        connection.execute(REMOVE_CHATID_QUERY, (chatid,))
        connection.commit()
        logging.info(f"Removed chat id to random message queue({chatid})")
    except Exception as e:
        logging.info(f"Failed to delete chatid({e})")


def setup():
    """setup things: create looper thread for queue and db connection"""
    global db_reader 
    global queue

    if not path.isfile(DB_PATH):
        db_reader = create_database()
    else:
        db_reader = db.connect(DB_PATH, check_same_thread=False)

    # add words in a thread safe way    
    threading.Thread(target=queue_handler, daemon=True).start()
    threading.Thread(target=message_scheduler_thread, daemon=True).start()

    # setup command handler
    commands.init(db_reader, queue)


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
        states={STATE_ADDWORD: [MessageHandler(Filters.text, commands.store_word)]},
        fallbacks=[]
    )

    add_custom_reply = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_CUSTOM_REPLY, commands.ask_custom_reply)],
        states=
            {
                STATE_ADD_QUERY:  [MessageHandler(Filters.text, commands.ask_custom_query)],
                STATE_ADD_ANSWER: [MessageHandler(Filters.text, commands.ask_custom_answer)]
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

    add_gif_handler = ConversationHandler(
        entry_points=[CommandHandler(COMMAND_ADD_GIF, commands.add_gif)],
        states={
            STATE_ADDGIF: [
                MessageHandler(Filters.animation, commands.store_gif)
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
    dispatcher.add_handler(add_gif_handler)
    dispatcher.add_handler(add_custom_reply)
    dispatcher.add_handler(InlineQueryHandler(commands.inlinequery))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_TEXT, commands.send_text))
    dispatcher.add_handler(CommandHandler(COMMAND_START, commands.start_handler))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_STICKER, commands.send_sticker))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_PHOTO, commands.send_photo))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_GIF, commands.send_gif))
    dispatcher.add_handler(CommandHandler(COMMAND_SEND_AUDIO, commands.send_music))
    dispatcher.add_handler(CommandHandler(COMMAND_ENABLE_RANDOM, commands.enable_random_messages))
    dispatcher.add_handler(CommandHandler(COMMAND_DISABLE_RANDOM, commands.disable_random_messages))
    dispatcher.add_handler(MessageHandler(Filters.text, commands.send_random_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, commands.direct_store_photo))
    
    
    logging.info('Telegram Random BOT started')
    updater.start_polling()
    updater.idle()



if __name__=='__main__':
    setup()
    main()
    if db_reader is not None: db_reader.close()
    if db_writer is not None: db_writer.close()


