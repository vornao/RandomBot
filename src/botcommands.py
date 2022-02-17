import logging
import sqlite3
import random

from queue import Queue
from functools import wraps
from uuid import uuid4

from telegram.ext import ConversationHandler, CallbackContext
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
<<<<<<< HEAD
<<<<<<< HEAD
from telegram import (
    InlineQueryResultCachedAudio,
=======
from telegram import (
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedPhoto,
    Update,
    InlineQueryResultArticle,
    InlineQueryResultCachedSticker,
)
<<<<<<< HEAD
=======
from telegram import InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto, Update, InlineQueryResultArticle, InlineQueryResultCachedSticker
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf

from const import *
from config import ALLOWED
from utils import *

import config as botreplies

QUEUE: Queue
DB_READER: sqlite3.Connection


def init(reader, q):
<<<<<<< HEAD
<<<<<<< HEAD
    global queue
    global db_reader
    queue = q
    db_reader = reader
=======
    global QUEUE 
=======
    global QUEUE
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
    global DB_READER
    QUEUE = q
    DB_READER = reader
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd



def restricted(handler):
    """If allowed list is not empty, will restrict access to specified user IDs"""

    @wraps(handler)
    def wrapped(update: Update, context, *args, **kwargs):
        user_id = None
        username = None

        # check if it's a message or an inline query
        try:
            user_id = update.message.from_user.id
            username = update.message.from_user.username
<<<<<<< HEAD
<<<<<<< HEAD
        except:
            pass

        try:
            user_id = update.inline_query.from_user.id
            username = update.inline_query.from_user.username
        except:
            pass

        if user_id not in ALLOWED and ALLOWED:
            logging.critical(
                f"UNAUTHORIZED USER TRIED TO ACCESS BOT! USERNAME: {username}, UID {user_id}"
            )
            return
=======
        except Exception as e: 
=======
        except Exception as e:
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
            logging.error(e)

        try:
            user_id = update.inline_query.from_user.id
            username = update.inline_query.from_user.username
        except Exception as e:
            logging.error(e)

        if user_id not in ALLOWED and ALLOWED:
            logging.critical(
                f"UNAUTHORIZED USER TRIED TO ACCESS BOT! USERNAME: {username}, UID {user_id}"
            )
            return None
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
        return handler(update, context)

    return wrapped


@restricted
def start_handler(update: Update, context: CallbackContext) -> None:
    """Handle /start command"""
    update.message.reply_text(botreplies.START_MSG)
    logging.info(
        "User Started BOT (User: %s, id: %d)",
        update.message.from_user.username,
        update.message.from_user.id,
    )


@restricted
def send_sticker(update: Update, context: CallbackContext):
    """Handle /sendsticker command"""
    update.message.reply_sticker(sticker=get_random_sticker(DB_READER, 1)[0])


@restricted
def send_photo(update: Update, context):
    """Handle /sendphoto command"""
    update.message.reply_photo(photo=get_random_photo(DB_READER, 1)[0])


@restricted
def send_text(update: Update, context):
    """Handle /sendphoto command"""
    update.message.reply_text(get_random_word(DB_READER, 1)[0])


@restricted
<<<<<<< HEAD
<<<<<<< HEAD
def send_music(update: Update, context):
    """Handle /sendmusic command"""
    update.message.reply_audio(audio=get_random_music(db_reader, 1)[0])
=======
def send_music(update: Update, context):    
    """Handle /sendmusic command"""    
=======
def send_music(update: Update, context):
    """Handle /sendmusic command"""
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
    update.message.reply_audio(audio=get_random_music(DB_READER, 1)[0])
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd



handlers = [send_text, send_photo, send_sticker, send_music]


@restricted
def send_random_message(update: Update, context: CallbackContext):
    """
    Handle simple message to bot and return random quote;
    There's 1/9 possibility that bot will return photo or audio instead of text
    """
    random.choices(handlers, (90, 20, 10, 20))[0](update, context)


@restricted
def add_word(update: Update, context: CallbackContext):
    """entry point for bot to add word"""
    update.message.reply_text(botreplies.ASK_WORD)
    return STATE_ONE


def store_word(update: Update, context: CallbackContext):
    """actually store word in db"""

<<<<<<< HEAD
<<<<<<< HEAD
    queue.put({"type": "word", "value": update.message.text})
=======
    QUEUE.put({'type' : 'word', 'value': update.message.text})
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
    QUEUE.put({"type": "word", "value": update.message.text})
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf

    update.message.reply_text(botreplies.CONTENT_ADDED_MSG)

    logging.info(
        "User Added Word! (User: %s, id: %d, Word: %s)",
        update.message.from_user.username,
        update.message.from_user.id,
        update.message.text,
    )

    return ConversationHandler.END


@restricted
def add_sticker(update, context):
    update.message.reply_text(botreplies.ASK_STICKERS)
    return STATE_ADDSTICKER


def store_sticker(update: Update, context):
<<<<<<< HEAD
<<<<<<< HEAD
    queue.put(
=======
    QUEUE.put(
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        {
            "type": "sticker",
            "uid": update.message.sticker.file_unique_id,
            "tid": update.message.sticker.file_id,
<<<<<<< HEAD
=======
    QUEUE.put({
        'type' : 'sticker',
        'uid': update.message.sticker.file_unique_id, 
        'tid': update.message.sticker.file_id
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        }
    )
    return STATE_ADDSTICKER


@restricted
def add_music(update, context):
    update.message.reply_text(botreplies.ASK_MUSIC)
    return STATE_ADDMUSIC


def store_music(update: Update, context):
<<<<<<< HEAD
<<<<<<< HEAD
    queue.put(
=======
    QUEUE.put(
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        {
            "type": "music",
            "uid": update.message.audio.file_unique_id,
            "tid": update.message.audio.file_id,
<<<<<<< HEAD
=======
    QUEUE.put({
        'type' : 'music',
        'uid': update.message.audio.file_unique_id, 
        'tid': update.message.audio.file_id
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        }
    )
    return STATE_ADDMUSIC


@restricted
def add_photo(update, context):
    update.message.reply_text(botreplies.ASK_PHOTOS)
    return STATE_ADDPHOTO


def store_photo(update: Update, context):
<<<<<<< HEAD
<<<<<<< HEAD
    queue.put(
=======
    QUEUE.put(
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        {
            "type": "photo",
            "uid": update.message.photo[1].file_unique_id,
            "tid": update.message.photo[1].file_id,
<<<<<<< HEAD
=======
    QUEUE.put({
        'type' : 'photo',
        'uid': update.message.photo[1].file_unique_id,
        'tid': update.message.photo[1].file_id
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        }
    )
    return STATE_ADDPHOTO


@restricted
def direct_store_photo(update: Update, context):
<<<<<<< HEAD
<<<<<<< HEAD
    queue.put(
=======
    QUEUE.put(
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        {
            "type": "photo",
            "uid": update.message.photo[1].file_unique_id,
            "tid": update.message.photo[1].file_id,
<<<<<<< HEAD
=======
    QUEUE.put({
        'type' : 'photo',
        'uid': update.message.photo[1].file_unique_id,
        'tid': update.message.photo[1].file_id
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        }
    )


def stop_conversation(update: Update, context):
    update.message.reply_text(botreplies.CONTENT_ADDED_MSG)
    return ConversationHandler.END


############################
### inline query handler ###
############################


def stickers_inline_query_result(update: Update):
    update.inline_query.answer(
        get_sticker_inline_result(6), cache_time=INLINE_CACHE_TIME
    )


def photos_inline_query_result(update: Update):
    update.inline_query.answer(get_photo_inline_result(6), cache_time=INLINE_CACHE_TIME)


def photo_inline_query_result(update: Update):
    update.inline_query.answer(get_photo_inline_result(1), cache_time=INLINE_CACHE_TIME)


def song_inline_query_result(update: Update):
    update.inline_query.answer(get_music_inline_result(1), cache_time=INLINE_CACHE_TIME)


def text_inline_query_result(update: Update):
    update.inline_query.answer(get_word_inline_result(1), cache_time=INLINE_CACHE_TIME)


funcs = [
    stickers_inline_query_result,
    photo_inline_query_result,
    song_inline_query_result,
    text_inline_query_result,
]


answers = {
    botreplies.INLINE_STICKER_QUERY: stickers_inline_query_result,
    botreplies.INLINE_PHOTO_QUERY: photos_inline_query_result,
    botreplies.INLINE_AUDIO_QUERY: song_inline_query_result,
}


def random_inline_query_result():
    return random.choices(funcs, (10, 20, 10, 90))[0]


@restricted
def inlinequery(update: Update, context: CallbackContext):
    """
    Handle inline query
    """
    query = update.inline_query.query

    # return random content if no valid query sumbitted.
    if query in answers:
        answers[query](update)
    else:
        random_inline_query_result()(update)


def get_music_inline_result(quantity: int) -> list:
<<<<<<< HEAD
<<<<<<< HEAD

    songs = get_random_music(db_reader, quantity)
=======
    
    songs =  get_random_music(DB_READER, quantity)
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======

    songs = get_random_music(DB_READER, quantity)
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf

    # using document to prevent bot from crashing when mp3 files have no title
    return [
        InlineQueryResultCachedDocument(
            id=uuid4(),
            title=botreplies.INLINE_AUDIO_REPLY_TITLE,
            description=botreplies.INLINE_AUDIO_REPLY_DESC,
            document_file_id=song,
        )
        for song in songs
    ]


def get_word_inline_result(quantity: int) -> list:
<<<<<<< HEAD
<<<<<<< HEAD

    quotes = get_random_word(db_reader, quantity)
    return [
=======
    
    quotes = get_random_word(DB_READER, quantity)
    return [ 
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======

    quotes = get_random_word(DB_READER, quantity)
    return [
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
        InlineQueryResultArticle(
            id=uuid4(),
            title=botreplies.INLINE_QUERY_REPLY,
            description=quote,
            input_message_content=InputTextMessageContent(quote),
        )
        for quote in quotes
    ]


def get_photo_inline_result(quantity: int) -> list:
<<<<<<< HEAD
<<<<<<< HEAD

    photos = get_random_photo(db_reader, quantity)
=======
    
    photos =  get_random_photo(DB_READER, quantity)
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======

    photos = get_random_photo(DB_READER, quantity)
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
    return [
        InlineQueryResultCachedPhoto(id=uuid4(), photo_file_id=photo)
        for photo in photos
    ]


def get_sticker_inline_result(quantity: int) -> list:
<<<<<<< HEAD
<<<<<<< HEAD
    stickers = get_random_sticker(db_reader, quantity)
=======
    stickers =  get_random_sticker(DB_READER, quantity)
>>>>>>> b67f1a0d5e4bbc74e212f138f6539ecccd1aecfd
=======
    stickers = get_random_sticker(DB_READER, quantity)
>>>>>>> 3324006ec274c916e53a6f4c98b8e2545697e0cf
    return [
        InlineQueryResultCachedSticker(id=uuid4(), sticker_file_id=sticker)
        for sticker in stickers
    ]
