import types
from config import *
from telebot import *
import datetime
from check_time import *


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


#new send message to admins
def send_message_to_admins( admins_id, text,parse_mode="HTML",disable_web_page_preview=True):
    for admin_id in admins_id:
        bot.send_message(
            chat_id=admin_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
   


@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name
    if is_user_in_chat(message.from_user.id):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        uz = types.KeyboardButton(text="O'zbek tili")
        ru = types.KeyboardButton(text='Русский язык')
        keyboard.add(uz,ru) 
        bot.send_message(
            chat_id = message.chat.id, 
            text = f" Привет {first_name} !", 
            )
        bot.send_message(
            chat_id = message.chat.id, 
            text = f"Tilni tanlang \ Выберите язык !", 
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

    #uzbek language
    if message.text == "O'zbek tili":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text="Keldim")
        exist = types.KeyboardButton(text='Bormayman')
        keyboard.add(button,exist) 
        bot.send_message(
            chat_id=message.chat.id,
            text = f"<b> Assalomu alaykum {first_name} !</b> ", 
            parse_mode="HTML",
            reply_markup=keyboard
            )
        
    elif message.text == "Keldim":
        #Запрашиваем причину позднего прихода
        if late_coming():
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id,
                text = 'Kechikish sababini yozing'
                )
            bot.register_next_step_handler(msg, process_reason_late_uz)
           
        else :   
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
            button = types.KeyboardButton(text="Kettim")
            keyboard.add(button)
         
            #send to admin
            # bot.send_message(
            #     chat_id=admin_id,
            #     text = f"Keldi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ", 
            #     parse_mode="HTML",
            #     disable_web_page_preview=True
            #     )

            #new send to admins 
            text = f"Keldi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ", 
            send_message_to_admins(admins_id=ADMIN_ID, text=text)
            
            #send to user
            bot.send_message(
                chat_id=message.chat.id,
                text = f"<b> Keldim: {current_time} </b> ", 
                reply_markup=keyboard,
                parse_mode="HTML"
                )

    elif message.text == "Kettim":
         #Запрашиваем причину раннего ухода
        if  early_leaving(): 
            
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id, 
                text = 'Erta ketish sababini yozing',
                )
            bot.register_next_step_handler(msg, process_reason_early_uz)
            
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button = types.KeyboardButton(text="Keldim")
            exist = types.KeyboardButton(text='Bormayman')
            keyboard.add(button,exist) 
            #send to admin
            # bot.send_message(
            #     chat_id=admin_id,
            #     text = f"Ketti: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
            #     parse_mode="HTML",
            #     disable_web_page_preview=True
            #     )

            #new send to admins
            text = f"Ketti: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
            send_message_to_admins(admins_id=ADMIN_ID, text=text)

            #send to user
            bot.send_message(
                chat_id=message.chat.id,
                text = f"<b> Kettim: {current_time} </b> ", 
                reply_markup=keyboard,
                parse_mode="HTML"
                )

    elif message.text == "Bormayman":
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id,
                text = 'Nega kelmasligingiz sababini yozing:'
                )
        
            bot.register_next_step_handler(msg, process_reason_exist_uz)
        

    #russion language
    if message.text == "Русский язык":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = types.KeyboardButton(text="Пришел")
        exist = types.KeyboardButton(text='Не приду')
        keyboard.add(button,exist) 
        bot.send_message(
            chat_id=message.chat.id,
            text = f"<b> Привет {first_name} !</b> ", 
            parse_mode="HTML",
            reply_markup=keyboard
            )
        
    elif message.text == "Пришел":
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
            # bot.send_message(
            #     chat_id=admin_id,
            #     text = f"Пришел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ", 
            #     parse_mode="HTML",
            #     disable_web_page_preview=True
            #     )

            #new send to admins
            text = f"Пришел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
            send_message_to_admins(admins_id=ADMIN_ID, text=text)

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
            exist = types.KeyboardButton(text='Не приду')
            keyboard.add(button,exist) 
            #send to admin
            # bot.send_message(
            #     chat_id=admin_id,
            #     text = f"Ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
            #     parse_mode="HTML",
            #     disable_web_page_preview=True
            #     )

            #new send to admins
            text = f"Ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{current_time}</b> ",
            send_message_to_admins(admins_id=ADMIN_ID, text=text)

            #send to user
            bot.send_message(
                chat_id=message.chat.id,
                text = f"<b> Ушел: {current_time} </b> ", 
                reply_markup=keyboard,
                parse_mode="HTML"
                )

    elif message.text == "Не приду":
            current_time = datetime.now().strftime("%H:%M")
            user_dict[message.chat.id] = User(current_time)
            msg = bot.send_message(
                chat_id = message.chat.id,
                text = 'Напишите причину почему не придете:'
                )
        
            bot.register_next_step_handler(msg, process_reason_exist)
        
#uzbek language
def process_reason_late_uz(message):
  
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
    button = types.KeyboardButton(text="Kettim")
    keyboard.add(button) 
    #send to admin
    bot.send_message(
        chat_id=admin_id,
        text = f"Kech qoldi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
        parse_mode="HTML",
        disable_web_page_preview=True
        )

    #new send to admins
    text = f"Kech qoldi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
    send_message_to_admins(admins_id=ADMIN_ID, text=text)
    
    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Keldim: {user.time} </b> ", 
        reply_markup=keyboard,
        parse_mode="HTML"
        )
    

def process_reason_early_uz(message):
  
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Keldim")
    exist = types.KeyboardButton(text='Bormayman')
    keyboard.add(button,exist) 
    #send to admin
    # bot.send_message(
    #     chat_id=admin_id,
    #     text = f"Erta ketti: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
    #     parse_mode="HTML",
    #     disable_web_page_preview=True
    #     )

    #new send to admins
    text = f"Erta ketti: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
    send_message_to_admins(admins_id=ADMIN_ID, text=text)

    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Kettim: {user.time} </b> ", 
        reply_markup=keyboard,
        parse_mode="HTML"
        )


def process_reason_exist_uz(message):
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    
    #send to admin
    # bot.send_message(
    #     chat_id=admin_id,
    #     text = f"Kelmadi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
    #     parse_mode="HTML",
    #     disable_web_page_preview=True
    #     )

    #new send to admins
    text = f"Kelmadi: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Sababi : {user.reason} ",
    send_message_to_admins(admins_id=ADMIN_ID, text=text)

    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Bormadim: {user.time} </b> ", 
        parse_mode="HTML"
        )


#russian language
def process_reason_late(message):
  
    user = user_dict[message.chat.id]
    user.reason = message.text
    first_name = message.from_user.first_name
    user_name = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
    button = types.KeyboardButton(text="Ушел")
    keyboard.add(button) 
    #send to admin
    # bot.send_message(
    #     chat_id=admin_id,
    #     text = f"Опаздал: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
    #     parse_mode="HTML",
    #     disable_web_page_preview=True
    #     )

    #new send to admins
    text = f"Опаздал: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
    send_message_to_admins(admins_id=ADMIN_ID, text=text)

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
    exist = types.KeyboardButton(text='Не приду')
    keyboard.add(button,exist) 
    #send to admin
    # bot.send_message(
    #     chat_id=admin_id,
    #     text = f"Рано ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
    #     parse_mode="HTML",
    #     disable_web_page_preview=True
    #     )

    #new send to admins
    text = f"Рано ушел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} "
    send_message_to_admins(admins_id=ADMIN_ID, text=text)

    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Ушел: {user.time} </b> ", 
        reply_markup=keyboard,
        parse_mode="HTML"
        )


def process_reason_exist(message):
    user = user_dict[message.chat.id]
    user.reason = message.text

    first_name = message.from_user.first_name
    user_name = message.from_user.username
    
    #send to admin
    # bot.send_message(
    #     chat_id=admin_id,
    #     text = f"Не пришел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} ",
    #     parse_mode="HTML",
    #     disable_web_page_preview=True
    #     )

    #new send to admins
    text = f"Не пришел: <a href=\"https://t.me/{user_name}\"> {first_name}</a> - <b>{user.time}</b> \n Причина : {user.reason} "
    send_message_to_admins(admins_id=ADMIN_ID, text=text)

    #send to user
    bot.send_message(
        chat_id=message.chat.id,
        text = f"<b> Не пришел: {user.time} </b> ", 
        parse_mode="HTML"
        )





if __name__ == '__main__':
    #new ''timeout=15,none_stop=True''
    bot.infinity_polling( timeout=15,none_stop=True )




