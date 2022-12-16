import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import os
from dotenv import load_dotenv 

load_dotenv()
secret_token = os.getenv('TOKEN')

updater = Updater(token=secret_token)
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'

def get_new_cat_image():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        print(error)      
        response = requests.get(URL_DOG)
    
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat 

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_cat_image())

def get_new_dog_image():
    try:
        response = requests.get(URL_DOG)
    except Exception as error:
        print(error)      
        response = requests.get(URL_CAT)
    
    response = response.json()
    random_dog = response[0].get('url')
    return random_dog 

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_dog_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['/cat', '/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Выбирай, на кого хочешь полюбоваться?'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_cat_image())
    context.bot.send_photo(chat.id, get_new_dog_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('cat', new_cat))
updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

updater.start_polling()
updater.idle()