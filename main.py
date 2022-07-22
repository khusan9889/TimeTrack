import types
from config import *
from telebot import *
import datetime
from check_time import *
import os
import pytz
import time


current_date = datetime.now(pytz.timezone('Asia/Tashkent'))


bot = telebot.TeleBot(TOKEN)
admin_id = ADMIN_ID
chat_id = CHAT_ID

member_list = ['creator', 'administrator', 'member']

user_dict = {}


class User:
    def __init__(self,time ):
        self.time = time
        self.reason = None
        

        

#function to check if the user is in chat
def is_user_in_chat(user_id, chat_id = chat_id):
    if bot.get_chat_member(chat_id, user_id).status in member_list:
        return True
    else:
        return False



@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name
    if is_user_in_chat(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text="Пришел")
        keyboard.add(button) 
        bot.send_message(
            chat_id = message.chat.id, 
            text = f" Привет {first_name} !", 
            reply_markup=keyboard
            ) 
    else:
        bot.delete_message(
            chat_id = message.chat.id, 
            message_id=message.message_id
            )
 


@bot.message_handler(content_types=["text"])
def keldi(message):
    first_name = message.from_user.first_name
    user_name = message.from_user.username
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    if message.text == "Пришел":
        #Запрашиваем причину позднего прихода
        if late_coming():
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id,
                text = 'Напишите причину позднего прихода'
                )
            bot.register_next_step_handler(msg, process_reason_late)
           
        else :   
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
            button = types.KeyboardButton(text="Ушел")
            keyboard.add(button)
         
            #send to admin
            bot.send_message(
                chat_id=admin_id,
                text = f"Пришел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ", 
                parse_mode="HTML",
                disable_web_page_preview=True
                )
            #send to user
            bot.send_message(
                chat_id=message.chat.id,
                text = f"<b> Пришел: {current_time} </b> ", 
                reply_markup=keyboard,
                parse_mode="HTML"
                )

    elif message.text == "Ушел":
         #Запрашиваем причину раннего ухода
        if early_leaving(): 
            
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id, 
                text = 'Напишите причину раннего ухода',
                )
            bot.register_next_step_handler(msg, process_reason_early)
            
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
            button = types.KeyboardButton(text="Пришел")
            keyboard.add(button) 
            #send to admin
            bot.send_message(
                chat_id=admin_id,
                text = f"Ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
                parse_mode="HTML",
                disable_web_page_preview=True
                )
            #send to user
            bot.send_message(
                chat_id=message.chat.id,
                text = f"<b> Ушел: {current_time} </b> ", 
                reply_markup=keyboard,
                parse_mode="HTML"
                )

def process_reason_late(message):
  
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
    button = types.KeyboardButton(text="Ушел")
    keyboard.add(button) 
    #send to admin
    bot.send_message(
        chat_id=admin_id,
        text = f"Опаздал: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
        parse_mode="HTML",
        disable_web_page_preview=True
        )
    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Пришел: {user.time} </b> ", 
        reply_markup=keyboard,
        parse_mode="HTML"
        )
    

def process_reason_early(message):
  
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
    button = types.KeyboardButton(text="Пришел")
    keyboard.add(button) 
    #send to admin
    bot.send_message(
        chat_id=admin_id,
        text = f"Рано ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
        parse_mode="HTML",
        disable_web_page_preview=True
        )
    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Ушел: {user.time} </b> ", 
        reply_markup=keyboard,
        parse_mode="HTML"
        )






if __name__ == '__main__':

    bot.infinity_polling()




