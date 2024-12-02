from Utils.Reader import BSMessageReader
from database.DataBase import DataBase
from Server.Login.LoginFailedMessage import LoginFailedMessage
import sqlite3 as sql
import random
import json


class DebugGems(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
         DataBase.replaceValue(self, 'gems', 9999)
         self.player.err_code = 1
         LoginFailedMessage(self.client, self.player, "[VIP] Gems updated: 9999").send()