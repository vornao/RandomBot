# Telegram Random Bot

This is a very simple bot that will reply to you with random quotes chosen from a database.
Bot will answer in private chat as well as group chats; inline commands are now fully supported!
This code has been written using python-telegram-bot library.

![CodeGrade](https://api.codiga.io/project/31355/status/svg)
![CodeScore](https://api.codiga.io/project/31355/score/svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---
### Requirements:
- Python 3.6.x
- pip
- python-telegram-bot (```pip install python-telegram-bot```)

---
### Installation instructions:
- Clone repository or download source files with ```git clone```
- Rename ```config.sample.py``` to ```config.py``` and replace values with your own custom configuration
- Create a bot with @botfather on telegram, then put your new token in ```config.py``` file. **Keep it a secret**.
- From @BotFather run ```/setinline``` to enable inline features and ```/setcommands``` in order to let telegram prompt your commands in the chat.
- From a terminal window now run: ```python3 randomBot.py &``` (the & command will leave it in background) or create Unit service for the script from systemd.
- If everything gone well, the bot is now running!
  
---
### Bot Usage instructions:
After the bot has started, it will reply to your messages with some random stuff from the database.  
- To add contents, use commands listed in ```config.py``` and follow instructions.
- This bot supports inline commands: type ```@your_bot_username``` in any chat to let him prompt you random quotes! (you can also ask for inline specific content, see config.sample.py)
- You can change bot settings from @BotFather. 
- [Further information on Telegram Offical Documentation](https://core.telegram.org/bots/api)

***

### 🔥 Changelog Ver. 0.2.1 🔥
- Now with support of adding and sending random stickers!

### 🔥 Changelog Ver. 1.0.0 🔥
- Now with images, audio, stickers support and improved efficiency with brand new database!
- Access control list improved
- Bug fix
