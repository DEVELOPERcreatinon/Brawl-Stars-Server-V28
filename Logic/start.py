import telebot 
import random 
import json
import os
import sqlite3
import psutil
from core import Server

# создаем бота
admin=[]
man=[]
bot = telebot.TeleBot('7268680838:AAFtJrzEomjtGD8hL_ZpiV5rsaH8gbgpGx4')

def dball():
    conn = sqlite3.connect("database/Player/plr.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM plrs")
    return cur.fetchall()

# Путь к файлу config.json
config_file_path = 'config.json'

def load_config():
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_config(config):
    try:
        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False

def update_maintenance_status(new_status):
    config = load_config()
    if config:
        config['maintenance'] = new_status
        return save_config(config)
    return False

def is_admin(user_id):
    return user_id in admin


# Структура для скинов
skins = {
    "common": [29, 15, 2, 103, 109, 167, 27, 120, 139, 111, 137, 152,],  # ID скинов
    "rare": [25, 102, 58, 98, 28, 92, 158, 130, 88, 165, 93, 104, 132, 108, 45, 125, 117, 11, 126, 131, 20, 100],
    "epic": [52, 159, 79, 64, 44, 123, 163, 91, 57, 160, 99, 30, 128, 71, 59, 26, 68, 147, 50, 75, 96, 110, 101, 118],
    "legendary": [94, 49, 95]
}

# Привязка цен к редкостям
skin_prices = {
    "common": (30, 30),
    "rare": (80, 80),
    "epic": (150, 150),
    "legendary": (300, 300)
}

# Функция для получения списка всех акций из файла offers.json
def get_offers():
    # Читаем данные из файла offers.json
    with open("Logic/offers.json", "r",encoding='utf-8') as f:
        data = json.load(f)

    # Генерируем текстовый список всех акци
    offer_list = "Список акций:\n"
    for offer_id, offer_data in data.items():
        vault=offer_data['ShopType']
        daily=offer_data['ShopDisplay']
        current=""
        types=""
        if vault==1:current="Золото"
        elif vault==0:current="Кристаллы"
        if daily==1:types="Ежедневная"
        elif daily==0:types="Обычная"
        offer_list += f"\nАкция #{offer_id}\n"
        offer_list += f"Название: {offer_data['OfferTitle']}\n"
        offer_list += f"Тип: {types}\n"
        offer_list += f"Боец: {offer_data['BrawlerID'][0]}\n"
        offer_list += f"Скин: {offer_data['SkinID'][0]}\n"
        offer_list += f"Валюта: {current}\n"
        offer_list += f"Стоимость: {offer_data['Cost']}\n"
        offer_list += f"Множитель: {offer_data['Multiplier'][0]}\n"

    # Возвращаем текстовый список всех акций
    return offer_list
# Обработчик команды /list
@bot.message_handler(commands=['list'])
def handle_list_offers(message):
    # Получаем список всех акций из файла offers.json
    offer_list = get_offers()

    # Отправляем пользователю список всех акций
    bot.send_message(chat_id=message.chat.id, text=offer_list)
    
    
@bot.message_handler(commands=['new_offer'])
def add_offer(message):
    user_id = message.from_user.id
    if user_id in admin:
    	if len(message.text.split()) < 2:
    	   bot.reply_to(message, 'Используйте команду /new_offer с аргументами в формате: /new_offer <ID> <OfferTitle> <Cost> <Multiplier> <BrawlerID> <SkinID> <OfferBGR> <ShopType> <ShopDisplay>')
    	   return
    	offer_data = message.text.split()
    	new_offer = {
            'ID': [int(offer_data[1]), 0, 0],
            'OfferTitle': offer_data[2],
            'Cost': int(offer_data[3]),
            'OldCost': 0,
            'Multiplier': [int(offer_data[4]), 0, 0],
            'BrawlerID': [int(offer_data[5]), 0, 0],
            'SkinID': [int(offer_data[6]), 0, 0],
            'WhoBuyed': [],
            'Timer': 86400,
            'OfferBGR': offer_data[7],
            'ShopType': int(offer_data[8]),
            'ShopDisplay': int(offer_data[9])
    	}
    	with open('Logic/offers.json', 'r',encoding='utf-8') as f:
    	   offers = json.load(f)
    	offers[str(len(offers))] = new_offer
    	with open('Logic/offers.json', 'w',encoding='utf-8') as f:
    	   json.dump(offers, f, indent=4)
    	bot.reply_to(message, 'Новая акция добавлена!')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
@bot.message_handler(commands=['panel_admin'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admin:
    	bot.reply_to(message, "Admin-Panel:\n----------------------\n/status - Проверить статус сервера.\n/theme - Изменить всем фон\n/new_code - Добавить новый код Автора.\n/del_code - Удалить код Автора.\n/code_list - Список кодов Автора.\n/auto_shop - Обновить ежедневынй магазин.\n/enable_maintenance - Включить тех.перерыв.\n/disable_maintenance -\nВыключить тех.перерыв.\n/change_name - Изменить имя игроку.\n/add_vip - Выдать вип статус./del_vip - Забрать вип статус.\n/add_gems - Выдать гемов\nигроку.\n/ban - Заблокировать игрока.\n/unban - Разблокировать игрока.\n/clear_room - Очистить румы в\nигре.\n/add_gold - Выдать монеты игроку.\n----------------------")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['panel_manager'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in man:
    	bot.reply_to(message, "Manager-Panel:\n----------------------\nДоступные команды:\n/gems - Выдача Гемов\n/prem - Выдать Вип\n/del_prem Удалить Вип Статус\n----------------------")
    else:
        bot.reply_to(message, "Вы не являетесь менеджером")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в бота для выдачи ShinyBrawl!\n/panel_manager - Команда для выдачи менеджеров\n/panel_admin - Полный управления сервером")

@bot.message_handler(commands=['change_name'])
def change_name(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /change_name ID NAME")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET name = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} изменили имя на {ammount}.")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['remove_offer'])
def remove_offer(message):
    user_id = message.from_user.id
    if user_id in admin:
    	if len(message.text.split()) != 2:
    	   bot.reply_to(message, 'Используйте команду /remove_offer с аргументом в формате: /remove_offer <ID>')
    	   return
    	offer_id = message.text.split()[1]
    	with open('Logic/offers.json', 'r', encoding='utf-8') as f:
    		offers = json.load(f)
    	if offer_id not in offers:
    		bot.reply_to(message, f'Акция с ID {offer_id} не найдена')
    		return
    	offers.pop(offer_id)
    	with open('Logic/offers.json', 'w', encoding='utf-8') as f:
    		json.dump(offers, f)
    	bot.reply_to(message, f'Акция с ID {offer_id} удалена')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
# Определяем функцию-обработчик для команды /theme
@bot.message_handler(commands=['theme'])
def theme(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Выбери ID темы\n0 - Обычная\n1 - Новый год (Снег)\n2 - Красный новый год\n3 - От клеш рояля\n4 - Обычный фон с дефолт музыкой\n5 - Желтые панды\n7 - Роботы Зелёный фон\n8 - Хэллуин 2019\n9 - Пиратский фон (Новый год 2020)\n10 - Фон с обновы с мистером п.\n11 - Футбольный фон\n12 - Годовщина Supercell\n13 - Базар Тары\n14 - Лето с монстрами\nИспользовать команду /theme ID")
        else:
            user_id = message.from_user.id
            theme_id = message.text.split()[1]
            conn = sqlite3.connect("database/Player/plr.db")
            c = conn.cursor()
            c.execute(f"UPDATE plrs SET theme={theme_id}")
            conn.commit()
            c.execute("SELECT * FROM plrs")
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Айди всех записей был изменён на {theme_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
#коды автора
@bot.message_handler(commands=['new_code'])
def new_code(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /new_code Название Кода(На англ)")
        else:
            code = message.text.split()[1]
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code not in config["CCC"]:
                config["CCC"].append(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Новый код {code}, Был добавлен!")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Код {code} уже существует!")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['code_list'])
def code_list(message):
    with open('config.json', 'r') as f:
        data = json.load(f)
    code_list = '\n'.join(data["CCC"])
    bot.send_message(chat_id=message.chat.id, text=f"Список кодов: \n{code_list}")
    	
    	
@bot.message_handler(commands=['del_code'])
def del_code(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /del_code Название Кода")
        else:
            code = message.text.split()[1]
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code in config["CCC"]:
                config["CCC"].remove(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Код {code}, Был удалён!")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Код {code} не найден!")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")
 #конец кодов
#Вип Старт
 
@bot.message_handler(commands=['add_vip'])
def add_vip(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_vip ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id not in config["vips"]:
                config["vips"].append(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был выдан игроку с ID {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус уже есть у ID {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['prem'])
def add_vip(message):
    user_id = message.from_user.id
    if user_id in man:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /prem ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id not in config["vips"]:
                config["vips"].append(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был выдан игроку с ID {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус уже есть у ID {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь менеджером!")
		
@bot.message_handler(commands=['del_vip'])
def del_vip(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /del_vip ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            code = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code in config["vips"]:
                config["vips"].remove(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был удален у игрока с ID {code}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус не найден у игрока с ID {code}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['del_prem'])
def del_vip(message):
    user_id = message.from_user.id
    if user_id in man:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /del_prem ID(Можно узнать в профиле профиле при поставке цветного ника)")
        else:
            code = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if code in config["vips"]:
                config["vips"].remove(code)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус был удален у игрока с ID {code}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Вип статус не найден у игрока с ID {code}")
    else:
        bot.reply_to(message, "Вы не являетесь менеджером!")

#Конец випов
@bot.message_handler(commands=['auto_shop'])
def auto_shop(message):
    user_id = message.from_user.id
    if user_id in admin:
        with open('Logic/offers.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for i in range(12): # изменяем первые 5 записей по ID
            if i <= 5:
                new_offer = {
                    'ID': [8, 0, 0],
                    'OfferTitle': "daily",
                    'Cost': random.randint(10, 228),
                    'OldCost': 0,
                    'Multiplier': [random.randint(1, 500), 0, 0],
                    'BrawlerID': [random.randint(1, 32), 0, 0],
                    'SkinID': [0, 0, 0],
                    'WhoBuyed': [],
                    'Timer': 86400,
                    'OfferBGR': "offer_gems",
                    'ShopType': 1,
                    'ShopDisplay': 1
                }
                # Выбираем редкость скина и устанавливаем соответствующую цену
                rarity = random.choice(['common', 'rare', 'epic', 'legendary'])
                cost = random.randint(*get_price_range_by_rarity(rarity))
                new_offer['Cost'] = cost
                
                skin_id = random.choice(get_skin_ids_by_rarity(rarity))
                new_offer['SkinID'] = [skin_id, 0, 0]
                data[i] = new_offer
            elif i > 5:
                with open('config.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                skins = settings['Skinse']
                random_skin = random.choice(skins)
                settings['Skinse'] = skins
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4, ensure_ascii=False)
                new_offer = {
                    'ID': [4, 0, 0],
                    'OfferTitle': "ЕЖЕДНЕВНЫЙ СКИН",
                    'Cost': 0,  # Добавляем поле Cost
                    'OldCost': 0,
                    'Multiplier': [0, 0, 0],
                    'BrawlerID': [0, 0, 0],
                    'SkinID': [random_skin, 0, 0],
                    'WhoBuyed': [],
                    'Timer': 86400,
                    'OfferBGR': "offer_gems",
                    'ShopType': 0,
                    'ShopDisplay': 0
                }
                # Выбираем редкость скина и устанавливаем соответствующую цену
                rarity = random.choice(['common', 'rare', 'epic', 'legendary'])
                cost = random.randint(*get_price_range_by_rarity(rarity))
                new_offer['Cost'] = cost
                
                skin_id = random.choice(get_skin_ids_by_rarity(rarity))
                new_offer['SkinID'] = [skin_id, 0, 0]
                data[i] = new_offer
        with open('Logic/offers.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        bot.reply_to(message, 'Акции успешно обновлены!')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

def get_skin_ids_by_rarity(rarity):
    # Словарь с идентификаторами скинов для каждой редкости
    skin_ids = {
        'common': [29, 15, 2, 103, 109, 167, 27, 120, 139, 111, 137, 152, 75],
        'rare': [25, 102, 58, 98, 28, 92, 158, 130, 88, 165, 93, 104, 132, 108, 45, 125, 117, 11, 126, 131, 20, 100],
        'epic': [52, 159, 79, 64, 44, 123, 163, 91, 57, 160, 99, 30, 128, 71, 59, 26, 68, 147, 50, 96, 110, 101, 118],
        'legendary': [94, 49, 95]
    }
    return skin_ids.get(rarity, [])  # Возвращает список идентификаторов скинов для указанной редкости, или пустой список, если редкость не найдена

def get_price_range_by_rarity(rarity):
    # Словарь с ценовыми диапазонами для каждой редкости
    price_ranges = {
        'common': (29, 30),
        'rare': (79, 80),
        'epic': (149, 150),
        'legendary': (299, 300)
    }
    return price_ranges.get(rarity, (10, 20))  # Возвращает ценовой диапазон для указанной редкости, или (10, 20) по умолчанию
		
# add_gems
@bot.message_handler(commands=['add_gems'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_gems ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET gems = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} Гемов")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['gems'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in man:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /gems ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET gems = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} Гемов")
    else:
        bot.reply_to(message, "Вы не являетесь менеджером!")
		
@bot.message_handler(commands=['ban'])
def ban(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /ban ID")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id not in config["banID"]:
                config["banID"].append(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Бан был выдан игроку {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Бан уже есть у игрока {vip_id}")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['unban'])
def ban(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /unban ID")
        else:
            vip_id = int(message.text.split()[1])
            with open("config.json", "r", encoding='utf-8') as f:
                config = json.load(f)
            if vip_id in config["banID"]:
                config["banID"].remove(vip_id)
                with open("config.json", "w", encoding='utf-8') as f:
                    json.dump(config, f, indent=4)
                bot.send_message(chat_id=message.chat.id, text=f"Разбан был выдан игроку {vip_id}")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"У игрока {vip_id} отсутствует бан")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['clear_room'])
def clear_room(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            user_id = message.from_user.id
            plrsinfo = "database/Player/plr.db"
            if os.path.exists(plrsinfo):
                conn = sqlite3.connect("database/Player/plr.db")
                c = conn.cursor()
                c.execute("UPDATE plrs SET roomID=0")
                c.execute("SELECT * FROM plrs")
                conn.commit()
                conn.close()
                bot.reply_to(message, 'Команды были очищены!')
            else:
                bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['add_trophies'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_trophies ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET trophies = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} Трофеев")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['add_gold'])
def add_gems(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Правильное использование /add_gold ID AMMOUNT")
        else:
            user_id = message.from_user.id
            id = message.text.split()[1]
            ammount = message.text.split()[2]
            conn = sqlite3.connect("database/Player/plr.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE plrs SET gold = ? WHERE lowID = ?", (ammount, id))
            conn.commit()
            conn.close()
            bot.send_message(chat_id=message.chat.id, text=f"Игроку с айди {id} Выдали {ammount} Монет!")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# Команда для обновления значения maintenance на true
@bot.message_handler(commands=['enable_maintenance'])
def enable_maintenance(message):
    if is_admin(message.from_user.id):
        if update_maintenance_status(True):
            bot.reply_to(message, "Технический перерыв был включен!")
        else:
            bot.reply_to(message, "Произошла ошибка при включении технического перерыва.")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# Команда для обновления значения maintenance на false
@bot.message_handler(commands=['disable_maintenance'])
def disable_maintenance(message):
    if is_admin(message.from_user.id):
        if update_maintenance_status(False):
            bot.reply_to(message, "Технический перерыв был выключен!")
        else:
            bot.reply_to(message, "Произошла ошибка при выключении технического перерыва.")
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if user_id in admin:
        if len(message.text.split()) < 2:
            user_id = message.from_user.id
            with open('config.json', 'r') as f:
                data = json.load(f)
                ban_list = len(data["banID"])
                vip_list = len(data["vips"])
            player_list = len(dball())
            bot.reply_to(message, f'Всего создано аккаунтов: {player_list}\nИгроков в бане: {ban_list}\nИгроков с вип: {vip_list}\n\nRAM: {psutil.virtual_memory().percent}%\nCPU: {psutil.cpu_percent()}%')
    else:
        bot.reply_to(message, "Вы не являетесь администратором!")

# Запускаем бота
bot.polling()