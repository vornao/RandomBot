STATE_ADDWORD = int(1)
STATE_ADDSTICKER = int(2)
STATE_ADDPHOTO = int(3)
STATE_ADDMUSIC = int(4)


USER_NOT_VALID = "You are not allowed to access this bot's contents."
USER_NOT_VALID_LOG = "Not allowed user tried to access bot! (User: %s, id: %d)"

INLINE_CACHE_TIME = 1


RANDOM_WORD_QUERY = "SELECT value FROM words ORDER BY random() LIMIT %d"
RANDOM_STICKER_QUERY = "SELECT value FROM stickers ORDER BY random() LIMIT %d"
RANDOM_PHOTO_QUERY = "SELECT value FROM images ORDER BY random() LIMIT %d"
RANDOM_MUSIC_QUERY = "SELECT value FROM music ORDER BY random() LIMIT %d"


CREATE_CHATS_TABLE_QUERY = """
    CREATE TABLE chats (
        id text NOT NULL PRIMARY KEY
    )
"""


CREATE_WORD_TABLE_QUERY = """
    CREATE TABLE words (
        hash text NOT NULL PRIMARY KEY,
        value text NOT NULL
    )
"""

CREATE_STICKER_TABLE_QUERY = """
    CREATE TABLE stickers (
        hash text NOT NULL PRIMARY KEY,
        value text NOT NULL
    )
"""

CREATE_IMAGES_TABLE_QUERY = """
    CREATE TABLE images (
        hash text NOT NULL PRIMARY KEY,
        value text NOT NULL
    )
"""

CREATE_MUSIC_TABLE_QUERY = """
    CREATE TABLE music (
        hash text NOT NULL PRIMARY KEY,
        value text NOT NULL
    )
"""

INSERT_WORD_QUERY = """
    INSERT INTO words
    VALUES (?, ?)
"""

INSERT_STICKER_QUERY = """
    INSERT INTO stickers
    VALUES (?, ?)
"""

INSERT_PHOTO_QUERY = """
    INSERT INTO images
    VALUES (?, ?)
"""

INSERT_MUSIC_QUERY = """
    INSERT INTO music
    VALUES (?, ?)
"""

INSERT_CHAT_QUERY = """
    INSERT INTO chats
    VALUES (?)
"""
