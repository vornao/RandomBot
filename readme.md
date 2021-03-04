# Telegram Random Bot
This is a very simple bot that will send you random quotes chosen from a text file.
 This code has been written using python-telegram-bot library.

### Requirements:
- Python 3.x
- python-telegram-bot (pip install python-telegram-bot)

### Installation instructions:
- Clone repository or download source files.
- Create a bot with @botfather on telegram, then put your new token in const.py file. Keep it secret.
- From a terminal window launch: python3 randomBot.py (to leave it in background you can put & at the end of the command.)
- If everything gone well, you can now start your bot from telegram!

### Bot Usage instructions:
After the bot has started, it will reply to your messages with some random stuff you put in words.txt file.
(Note: on @BotFather run /setinline to let telegram prompt out your commands)
- /start will start the bot
- /sendmessage will make the bot send you a message 
- /addword will let you add words to words.txt file without editing the file from a shell
- This bot supports inline commands: type @your_bot_username in any chat to let him prompt you random stuff!
  (you have to enable inline mode from BotFather)

