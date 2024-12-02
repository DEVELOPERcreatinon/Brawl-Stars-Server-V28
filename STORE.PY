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
    markup.add(InlineKeyboardButton("МАГАЗИН 😇", callback_data="shop"),
               InlineKeyboardButton("ИНФОРМАЦИЯ 🔥", callback_data="news"),
               InlineKeyboardButton("ТЕХ ПОДДЕРЖКА 🟢", callback_data="help"))
    return markup
    
def news_button():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🏆 НОВОСТИ", callback_data="news"),
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
    markup.add(InlineKeyboardButton("🌟 ТОВАРЫ", callback_data="item"),
               InlineKeyboardButton("🌟 ТЕГИ", callback_data="teg"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup

def shop_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2 
    markup.add(InlineKeyboardButton("🌟 ТОВАРЫ", callback_data="item"),
               InlineKeyboardButton("🥳 ТЕГИ", callback_data="teg"),
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
    markup.add(InlineKeyboardButton("🥰 КУПИТЬ @NEVETI", callback_data="buy"),
               InlineKeyboardButton("- НАЗАД", callback_data="back"))
    return markup
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "back":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "ПРИВЕТ 🔥", reply_markup=gen_markup())
    elif call.data == "accloud":
        bot.answer_callback_query(call.id, "❌ АККАУНТЫ В РАЗРАБОТКЕ")
    elif call.data == "help":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="НУЖНА ПОМОЩЬ? ВОПРОСЫ?\nНАПИШИ МНЕ В ЛС И УЗНАЙ ОТВЕТ\nНА СВОЙ ВОПРОС - @NEVETI", reply_markup=back_button())
    elif call.data == "shop":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ЭТО МАГАЗИН ТГ! ОБЯЗАТЕЛЬНО ИЗМЕНИ ТЕКСТ.\n\nТУТ К ПРИМЕРУ ГЕМЫ \nПРИМЕР 500 ГЕМОВ- 800Р\n\nИ ТАК ДАЛЕЕ ВЫБЕРИТЕ САМИ)", reply_markup=shop_button())
    elif call.data == "buy":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔥 ВЫ ЧТО ТО ЗАХОТЕЛИ КУПИТЬ?\nНАПИШИ МНЕ ТЫ ХОТЕЛ КУПИТЬ!\n@NEVETI ❗", reply_markup=back_button())
    elif call.data == "news":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🥳 СЛЕДИ ЗА СЕРВЕРОМ У НАС В КАНАЛЕ!\n- ТАМ МОЖНО УЗНАТЬ ДАТУ ОБНОВЛЕНИЯ!\nИ МНОГОЕ ДРУГОЕ @FROSTSTARSBIZZARE", reply_markup=back_button())   
#Shop Menu
    elif call.data == "item":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" ➖ SHOP ITEMS ➖\n -\n 1. TEST_ITEM1\n 2. TEST_ITEM2\n 3. TEST_ITEM3\n 4. TEST_ITEM4", reply_markup=shop_item_menu())   
    elif call.data == "teg":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" - SHOP TEGS ❤️‍🔥 -\n\n 1. TEST_TEG1\n 2. TEST_TEG2\n 3. TEST_TEG3\n 4. TEST_TEG4", reply_markup=shop_teg_menu())   
###
    elif call.data == "":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🥳 SHOP TEGS", reply_markup=shop_teg_menu())   

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.reply_to(message, "🔥", reply_markup=gen_markup())
     
bot.infinity_polling()
