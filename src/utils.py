import logging
import sqlite3
from const import *
from config import PATH_LOG

USER_NOT_VALID = "You are not allowed to access this bot's contents."
USER_NOT_VALID_LOG = "Not allowed user tried to access bot! (User: %s, id: %d)"

logging.basicConfig(
    filename=PATH_LOG, 
    filemode="a", 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level = logging.INFO)


def get_random_word(conn: sqlite3.Connection, limit: int) -> list:
    cur = conn.execute(RANDOM_WORD_QUERY % limit)
    res = cur.fetchall()
    val = [r[0] for r in res]
    return val

def get_random_sticker(conn: sqlite3.Connection, limit: int) -> str:
    cur = conn.execute(RANDOM_STICKER_QUERY % limit)
    res = cur.fetchall()
    val = [r[0] for r in res]
    return val

def get_random_photo(conn: sqlite3.Connection, limit: int) -> str:
    cur = conn.execute(RANDOM_PHOTO_QUERY % limit)
    res = cur.fetchall()
    val = [r[0] for r in res]
    return val

def get_random_music(conn: sqlite3.Connection, limit: int) -> str:
    cur = conn.execute(RANDOM_MUSIC_QUERY % limit)
    res = cur.fetchall()
    val = [r[0] for r in res]
    return val

def get_random_gif(conn: sqlite3.Connection, limit: int) -> str:
    cur = conn.execute(RANDOM_GIF_QUERY % limit)
    res = cur.fetchall()
    val = [r[0] for r in res]
    return val

class CustomQueryDataHolder:
    def __init__(self, query: str, ans: str):
        self.query = query
        self.answer = ans

def get_custom_reply(conn: sqlite3.Connection, limit: int, query: str):
    cur = conn.execute(CUSTOM_REPLY_QUERY, (query,))
    res = cur.fetchall()
    if len(res) > 0:
        return res[0]
    else:
        return None



 