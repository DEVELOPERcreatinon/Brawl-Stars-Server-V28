import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import threading
from requests import get
from time import sleep

token = 'YOUR_BOT_TOKEN' #ТОКЕН БОТА

bot = telebot.TeleBot(token)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Магазин", callback_data="shop"),
               InlineKeyboardButton("Информация", callback_data="news"),
               InlineKeyboardButton("Тех Поддержка", callback_data="help"))
    return markup
    
def news_button():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Новости", callback_data="news"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup 

def back_button():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup
    
def shop_button():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("Кристаллы", callback_data="item"),
               InlineKeyboardButton("Vip-status", callback_data="teg"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("Кристаллы", callback_data="item"),
               InlineKeyboardButton("Vip-status", callback_data="teg"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup

def shop_item_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("🌟 КУПИТЬ ТОВАР", callback_data="buy"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup

def shop_teg_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("🌟 КУПИТЬ ТОВАР", callback_data="buy"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "back":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "Добро пожаловать! Это официальный магазин Shiny Brawl.", reply_markup=gen_markup())
    elif call.data == "accloud":
        bot.answer_callback_query(call.id, "❌ АККАУНТЫ В РАЗРАБОТКЕ")
    elif call.data == "help":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Техническая Поддержка @ShinySupportRobot", reply_markup=back_button())
    elif call.data == "shop":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Меню магазина:", reply_markup=shop_button())
    elif call.data == "buy":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Купить товар — @VerixDev", reply_markup=back_button())
    elif call.data == "news":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Телеграм Канал — @ShinyServers\nТехническая Поддержка — @ShinySupportRobot\n\nПо вопросам @VerixDev", reply_markup=back_button())   
#Shop Menu
    elif call.data == "item":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Прайс гемов:\n\n30 гемов— 15₽\n80 гемов— 40₽\n170 гемов— 70₽\n360 гемов— 100₽\n950 гемов— 300₽\n2000 гемов— 500₽\n5000 гемов - 1000₽", reply_markup=shop_item_menu())   
    elif call.data == "teg":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Прайс VIP-status:\n\nVIP - Статус который дает преимущества:\nx2 кубки, скин МАЙК-ПОВАР\n30 гемов", reply_markup=shop_teg_menu())   
###
    elif call.data == "":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🥳 SHOP TEGS", reply_markup=shop_teg_menu())   

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.reply_to(message, "Добро пожаловать! Это официальный магазин Shiny Brawl.", reply_markup=gen_markup())
     
bot.infinity_polling()
