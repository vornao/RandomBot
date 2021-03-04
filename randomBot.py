#a simple python bot that will send random contents

#ver 0.1.3
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from telegram.parsemode import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, InlineQueryHandler
from telegram import Update, InlineQueryResultArticle
from uuid import uuid4
import logging, random
from const import *

#put here your words file path

p_list = []

#logging setup
logging.basicConfig(
    filename="b0t.log", 
    filemode="a", 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level = logging.INFO)


def start_handler(update, context, p_list: list) -> None: 
    update.message.reply_text("Hello!")
    logging.info("User Started BOT (User: %s, id: %d)", 
        update.message.from_user.username, 
        update.message.from_user.id)

def send_message(update, context) -> None:
    update.message.reply_text(random.choice(p_list))

        
#step one of conversation: user is asked to send a word to add.
#                todo do not add duplicates                  #

def add_p_word(update, context):
    update.message.reply_text("Send me something!")
    return STATE_ONE

#step two of conversation: word is stored in main memory and in words.txt file for reuse
def store_p_word(update, context):

    #add word to local list
    p_list.append(update.message.text)

    #open file and append word
    with open(WORDS_PATH, "a") as words_file:
        words_file.write('\n')
        words_file.write(update.message.text)

    update.message.reply_text("Done.")

    logging.info("User Added Word! (User: %s, id: %d, Word: %s)", 
            update.message.from_user.username, 
            update.message.from_user.id, 
            update.message.text)
    return ConversationHandler.END

#Handles inline queries. No need for user to type anything, random message will prompt
def inlinequery(update, context):
    ans = random.choice(p_list)
    update.inline_query.answer([ 
        InlineQueryResultArticle(
            id=uuid4(),
            title="Random Quote",
            description=ans,
            input_message_content = InputTextMessageContent(ans, parse_mode=ParseMode.MARKDOWN)
            )
        ])


#main method, initialize context and starts bot.
def main():
    try: 
        word_file = open(WORDS_PATH, "r")
        temp_list = word_file.read().splitlines()
        for x in temp_list:
            p_list.append(x)
    except:
        logging.error("error opeining words.txt")
    finally:
        word_file.close()

    logging.info("Words File loaded!")
    
    updater = Updater(TOKEN, use_context = True)
    dispatcher = updater.dispatcher

    #add words handler function
    add_word_handler = ConversationHandler(
        entry_points=[
            CommandHandler("addword", add_p_word)],
        states={
            STATE_ONE: [
                MessageHandler(Filters.text, store_p_word)
                ]
            },
        fallbacks=[]
    )

    dispatcher.add_handler(add_word_handler)
    #welcome message handler
    dispatcher.add_handler(CommandHandler("start", start_handler))

    #will answer with random words at every message
    dispatcher.add_handler(MessageHandler(Filters.text, send_message))

    #inline query handler from telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    #will send random word without receiving message
    dispatcher.add_handler(CommandHandler("sendmessage", send_message))

    logging.info("Telegram bot started")
    print("Telegram bot started")
    updater.start_polling()

    #for graceful termination send CTRL+C or SIGINT to process
    updater.idle()
    

if __name__=='__main__':
    main()
