from Server.Login.LoginOkMessage import LoginOkMessage
from Server.Home.OwnHomeDataMessage import OwnHomeDataMessage 
from Server.Team.TeamMessage import TeamMessage
from Server.Login.LoginFailedMessage import LoginFailedMessage
from Utils.Reader import BSMessageReader
from Utils.Helpers import Helpers
from database.DataBase import DataBase
from database.DevMessage import DevMessage
from Server.Club.AllianceStreamMessage import AllianceStreamMessage
from Server.Club.MyAllianceMessage import MyAllianceMessage
import os
from Server.Friend.FriendListMessage import FriendListMessage

import json
class LoginMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.player.high_id = self.read_int()
        self.player.low_id = self.read_int()
        self.player.token = self.read_string()
        self.major = self.read_int()
        self.minor = self.read_int()
        self.build = self.read_int()

    def process(self):
        config = open('config.json', 'r')
        content = config.read()
        settings = json.loads(content)
        if self.player.low_id in settings['banID']:
            print("banned")
            update_url = 'https://t.me/ksdbrawl'
            self.player.err_code = 11
            LoginFailedMessage(self.client, self.player, "Упс, кажись вы были заблокированы навсегда! Ошибка? Подать на аппеляцию можно написав админу - @DZDZDZ123rt").send()

        if settings['maintenance'] != False:
            self.player.err_code = 10
            LoginFailedMessage(self.client, self.player, "").send()
        
        if self.player.low_id == 0:
            plrsinfo = "database/Player/plr.db"
            if os.path.exists(plrsinfo):
                self.player.low_id = 2+(len(DataBase.getAll(self)))
            else:
                self.player.low_id = 2
            self.player.token = Helpers.randomStringDigits(self)
            self.player.high_id = 0
            LoginOkMessage(self.client, self.player).send()
            DataBase.createAccount(self)
            OwnHomeDataMessage(self.client, self.player).send()
        DataBase.loadAccount(self)
        if self.player.low_id >= 2:
            LoginOkMessage(self.client, self.player).send()
            OwnHomeDataMessage(self.client, self.player).send()
            try:
                MyAllianceMessage(self.client, self.player, self.player.club_low_id).send()
                AllianceStreamMessage(self.client, self.player, self.player.club_low_id, 0).send()
                DataBase.GetmsgCount(self, self.player.club_low_id)
            except:
                MyAllianceMessage(self.client, self.player, 0).send()
                AllianceStreamMessage(self.client, self.player, 0, 0).send()
            FriendListMessage(self.client, self.player).send()
            DevMessage(self.client, self.player).send()
        else:
            self.player.err_code = 8
            LoginFailedMessage(self.client, self.player, "Аккаунт не найден удалите все данные о игре!").send()