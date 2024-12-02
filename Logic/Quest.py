import json
import sqlite3

class Quest:
    def EncodeQuest(self):
        self.writeBoolean(True)  # Quests Boolean
        
        with sqlite3.connect('database/Player/plr.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM plrs WHERE lowID=?', (self.player.low_id,))
            user = cursor.fetchone()

            if user is None:
                # Обработка случая, когда пользователь не найден
                self.writeVint(0)
                return
            
            quests = user[29]  # Предполагается, что это уже JSON-строка
            if quests:
                quests = json.loads(quests)
            else:
                quests = []

            questsCount = sum(1 for i in quests if i["state"] == 0)

            self.writeVint(questsCount)

            if questsCount > 0:
                for item in quests:
                    if item["state"] == 0:  # Обрабатываем только активные квесты
                        self.writeVint(0)  # Плейсхолдер или индекс предмета
                        self.writeVint(1)  # Тип миссии
                        self.writeVint(item['counts'])  # Текущая цель квеста
                        self.writeVint(item['win_count'])  # Максимальная цель квеста
                        self.writeVint(item['prize'])  # Награда токенами
                        self.writeVint(0)  # Плейсхолдер
                        self.writeVint(0)  # Текущий уровень
                        self.writeVint(0)  # Максимальный уровень
                        self.writeVint(item['QT'])  # Тип квеста
                        self.writeBoolean(False)  # Эксклюзив для Brawl Pass
                        self.writeScId(16, item['id'])  # ID Бравлера
                        self.writeVint(item['GM'])  # ID игрового режима
                        self.writeVint(0)
            else:
                self.writeVint(0)  # Нет активных квестов