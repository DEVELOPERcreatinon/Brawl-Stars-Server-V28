from Utils.Writer import Writer
from database.DataBase import DataBase
from Logic.Player import Players
from Utils.Helpers import Helpers

class TeamLeaveOkMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24125
        self.player = player

    def encode(self):
        self.writeHexa('''00000000''')
        self.player.room_id = 0