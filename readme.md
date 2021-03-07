# Telegram Random Reply Bot
This is a very simple (experimental) bot that will reply to you with random quotes chosen from a text file.
Bot will answer messages in private chat as well as group chat replies.
This code has been written using python-telegram-bot library.

### Requirements:
- Python 3.x
- pip
- python-telegram-bot (```pip install python-telegram-bot```)
### Installation instructions:
- Clone repository or download source files with ```git clone (...)```
- Create a bot with @botfather on telegram, then put your new token in ```const.py``` file. **Keep it a secret**.
- From @BotFather run ```/setinline``` to enable inline features and ```/setcommands``` in order to let telegram prompt your commands in the chat.
- From a terminal window now run: ```python3 randomBot.py &``` ( the & command will leave it in background)
- If everything gone well, the bot is now running!
### Bot Usage instructions:
After the bot has started, it will reply to your messages with some random stuff you put in words.txt file.  
- ```/start``` will start the bot
- ```/sendmessage``` will make the bot send you a random message to reply (useful in groups)
- ```/addword``` will let you add words to words.txt file without editing the file from a shell, follow instructions.
- This bot supports inline commands: type ```@your_bot_username``` in any chat to let him prompt you random stuff!
- ✨ Will soon support sending random media and stickers! ✨
- You can change bot settings from @BotFather. 
- [Further information on Telegram Offical Documentation](https://core.telegram.org/bots/api)

***

### 🔥 Changelog Ver. 0.2.1 🔥
- Now with support of adding and sending random stickers!


