# RENAME THIS FILE AS secrets.py

# Place here your bot token (get it from bot father)
TELEGRAM_BOT_TOKEN = "BOT-TOKEN-HERE"

# list empty, everyone can access bot
ALLOWED = []

# list not empty, access granted to specified users only
# uncomment and put user ids here (not usernames)
# ALLOWED = [userid1, userid2]

PATH_LOG = "../files/random-bot.log"
DB_PATH = "../files/random-bot.sqlite"


################################################
### Customize bot replies and commands here! ###
################################################

# message for /start command
START_MSG = "Random Bot started!"
START_CHAT_MSG = "Server restarted"


TOGGLE_BOT_KEYWORD = ["ciao bot", "Ciao bot"]
TOGGLE_BOT_ANSWERS = ["bot enabled!", "hello there!"]

# answer when conversation ends
CONTENT_ADDED_MSG = "Done!"
PHOTO_ADDED_REPLY = ["photo added!"]
GIF_ADDED_REPLY = ["gif added!"]

# replies for /add* commands
ASK_WORD = "Send me a new quote!"
ASK_STICKERS = "Send me stickers! type /stop when you're done"
ASK_MUSIC = "Send me audio files! type /stop when you're done"
ASK_PHOTOS = "Send me photos! type /stop when you're done"
ASK_GIF = "Send me gifs! Type /stop when you're done"

COMMAND_SEND_TEXT = "sendmessage"
COMMAND_SEND_PHOTO = "sendphoto"
COMMAND_SEND_STICKER = "sendsticker"
COMMAND_SEND_AUDIO = "sendaudio"
COMMAND_START = "start"
COMMAND_END = "stop"
COMMAND_ENABLE_RANDOM = "enablerandomscheduling"
COMMAND_DISABLE_RANDOM = "stopscheduling"
COMMAND_SEND_GIF = "sendgif"

COMMAND_ADD_TEXT = "addword"
COMMAND_ADD_PHOTO = "addphoto"
COMMAND_ADD_STICKER = "addsticker"
COMMAND_ADD_AUDIO = "addmusic"
COMMAND_ADD_GIF = "addgif"

INLINE_PHOTO_QUERY = "pic"
INLINE_AUDIO_QUERY = "music"
INLINE_STICKER_QUERY = "sticker"

INLINE_QUERY_REPLY = "Random quote from RandomBot"
INLINE_AUDIO_REPLY_TITLE = "Random song!"
INLINE_AUDIO_REPLY_DESC = "Fantastic random song!"
INLINE_GIF_QUERY = "gif"
