
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, InlineQueryHandler
from telegram import Update, InlineQueryResultArticle, InlineQueryResultCachedSticker
from uuid import uuid4
from utils import *
import logging, random
from const import *
from utils import *

#put here your bot api token
TOKEN = TOKEN
p_list = []
stickers_list = []
stickers_uids = []
allowed = []
stickers_dict = {}

logging.basicConfig(
    filename='b0t.log', 
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level = logging.INFO)

#main method, load files specified in utils.py and starts bot.
def main():
    load_file_to_list(PATH_TO_WORDS, p_list)
    load_file_to_list(PATH_TO_STICKERS, stickers_list)
    load_file_to_list(PATH_TO_STICKERS_UIDS, stickers_uids)
    parse_csv(PATH_TO_STICKER_MAP, stickers_dict)
    print(stickers_dict)

    logging.info('Files loaded!')
    
    updater = Updater(TOKEN, use_context = True)
    dispatcher = updater.dispatcher

    add_word_handler = ConversationHandler(
        entry_points=[CommandHandler('addword', add_word)],
        states={ STATE_ONE: [MessageHandler(Filters.text, store_p_word)]
            },
        fallbacks=[]
    )

    add_sticker_handler = ConversationHandler(
        entry_points=[CommandHandler('addsticker', add_sticker)],
        states={
            STATE_ADDSTICKER: [
                MessageHandler(Filters.sticker, store_sticker)
                ]
            },
        fallbacks=[CommandHandler('stop', stop_add_sticker)]
        )

    dispatcher.add_handler(add_word_handler)
    dispatcher.add_handler(add_sticker_handler)
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    dispatcher.add_handler(CommandHandler('sendmessage', send_message))
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('sendsticker', send_sticker))
    dispatcher.add_handler(MessageHandler(Filters.text, send_message))
    
    
    logging.info('Telegram B0T started')
    updater.start_polling()
    updater.idle()


def start_handler(update: Update , context: CallbackContext) -> None:
    update.message.reply_text('Welcome to random bot!')
    logging.info('User Started BOT (User: %s, id: %d)', 
        update.message.from_user.username, 
        update.message.from_user.id)

    
def send_message(update: Update , context: CallbackContext):
    update.message.reply_text(random.choice(p_list))
        
def add_word(update: Update, context: CallbackContext):
    update.message.reply_text('Send me a funny quote!')
    return STATE_ONE
        
#step two of conversation: word is stored in main memory and in words.txt file for reuse
def store_p_word(update: Update, context: CallbackContext):

    p_list.append(update.message.text)
    append_to_file(PATH_TO_WORDS, update.message.text)

    update.message.reply_text('Done!')

    logging.info('User Added Word! (User: %s, id: %d, Word: %s)', 
            update.message.from_user.username, 
            update.message.from_user.id, 
            update.message.text)

    return ConversationHandler.END

#Block of functions to handle sticker store and sending
def add_sticker(update, context):
    update.message.reply_text('Send me funny stickers! Type /stop when you\'re done')
    return STATE_ADDSTICKER

def store_sticker(update: Update, context):
    #combining uniques ids and private ids to avoid duplicates!
    if(update.message.sticker.file_unique_id not in stickers_dict.keys()):
        stickers_dict[update.message.sticker.file_unique_id] = update.message.sticker.file_id
        append_to_csv(
            PATH_TO_STICKER_MAP, 
            update.message.sticker.file_unique_id, 
            update.message.sticker.file_id)
    return STATE_ADDSTICKER

def stop_add_sticker(update: Update, context):
    update.message.reply_text('Done!')
    return ConversationHandler.END

def send_sticker(update: Update, context: CallbackContext):
    #can be a bottleneck, to review.
    update.message.reply_sticker(sticker=random.choice(list(stickers_dict.values())))


#Handles inline queries. No need for user to type anything, random message will prompt
def inlinequery(update: Update, context: CallbackContext):

    query = update.inline_query.query

    if (query == 'sticker'):
        #same as before, list constructor can be bottleneck. to review.
        stickers = random.choices(list(stickers_dict.values()), k=4)
        update.inline_query.answer([
            InlineQueryResultCachedSticker(
            id=uuid4(),
            sticker_file_id = sticker
            )  for sticker in stickers
        ])
    else:
        quote = random.choice(p_list)
        update.inline_query.answer([ 
            InlineQueryResultArticle(
                id=uuid4(),
                title='Random quote:',
                description=quote,
                input_message_content = InputTextMessageContent(quote)
                ),
            ])
    
#start main thread
if __name__=='__main__':
    main()