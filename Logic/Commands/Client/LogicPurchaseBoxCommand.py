from database.DataBase import DataBase
from Logic.Commands.Client.LogicBoxDataCommand import LogicBoxDataCommand
from Logic.MCbyLkPrtctrd.MilestonesClaimSupplyByLkPrtctrd import MilestonesClaimSupplyByLkPrtctrd as Supply
from Utils.Reader import BSMessageReader

class LogicPurchaseBoxCommand(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.a = self.read_Vint()
        self.b = self.read_Vint()
        self.c = self.read_Vint()
        self.d = self.read_Vint()
        self.boxid = self.read_Vint()


    def process(self):
        if self.boxid == 6:
            self.boxid = 10
        elif self.boxid == 7:
            self.boxid = 12
        elif self.boxid == 8: 
            self.boxid = 11
        elif self.boxid == 5:  # Brawl Box
            self.player.box = self.player.box - 100
            DataBase.replaceValue(self, 'box', self.player.box)
            self.boxid = 10
        elif self.boxid == 4:  # Big Box
            self.player.bigbox = self.player.box - 30
            DataBase.replaceValue(self, 'bigbox', self.player.bigbox)
            self.boxid = 12
        elif self.boxid == 3:  # Shop Box
            self.player.gems = self.player.gems - 30
            DataBase.replaceValue(self, 'gems', self.player.gems)
            self.boxid = 11
        elif self.boxid == 1:  # Shop Big Box
            self.player.gems = self.player.gems - 30
            DataBase.replaceValue(self, 'gems', self.player.gems)
            self.boxid = 12
        elif self.boxid == 4:  # Shop Mega Box
            self.player.gems = self.player.gems - 80
            DataBase.replaceValue(self, 'gems', self.player.gems)
            self.boxid = 11
        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": self.boxid}).send()