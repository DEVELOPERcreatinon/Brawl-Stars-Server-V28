from database.DataBase import DataBase
from Logic.LogicBuy import LogicBuy

from Utils.Reader import BSMessageReader
from Logic.MCbyLkPrtctrd.MilestonesClaimSupplyByLkPrtctrd import MilestonesClaimSupplyByLkPrtctrd
class LogicViewNotificationCommand(BSMessageReader):
    def __init__(self, client, player, initial_bytes,id,k,bp,id2=0):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.a = self.read_Vint()
        self.b = self.read_Vint()
        self.c = self.read_Vint()
        self.d = self.read_Vint()
        self.notif = self.read_Vint()


    def process(self):
        if self.notif == 2281337:
            MilestonesClaimSupplyByLkPrtctrd(self.client, self.player, "BPLkPrtctrd", {"Character": [1,1], "Skin": [135,135],"Type":9,"Amount": 1, "Road": 0, "Season": 0, "Level": -2}).send()
            self.player.notifRead = True
            DataBase.replaceValue(self, 'notifRead', self.player.notifRead)

        if self.notif == 2281778:
            MilestonesClaimSupplyByLkPrtctrd(self.client, self.player, "BPLkPrtctrd", {"Character": [0, 0], "Skin": [0, 0],"Type":8,"Amount": 30, "Road": 0, "Season": 0, "Level": -2}).send()
            self.player.notifRead2 = True
            DataBase.replaceValue(self, 'notifRead2', self.player.notifRead2)