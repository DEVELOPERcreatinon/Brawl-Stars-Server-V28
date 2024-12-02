from Server.Team.TeamMessage import TeamMessage
from database.DataBase import DataBase
from Files.CsvLogic.Characters import Characters

from Utils.Reader import BSMessageReader
from Utils.G import Gameroom


class TeamChangeBrawlerMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.csv_id = self.read_Vint()
        if self.csv_id == 23:
            self.StarpowerID = self.read_Vint()
        else:
            self.csv_id = self.read_Vint()
            self.BrawlerSkinId = self.read_Vint()

    def process(self):
        if self.csv_id == 29:
            self.player.brawler_id = Characters.get_brawler_by_skin_id(self, self.BrawlerSkinId)
        self.player.skin_id = self.BrawlerSkinId
        DataBase.replaceValue(self, 'skinID', self.player.skin_id)
        DataBase.replaceValue(self, 'brawlerID', self.player.brawler_id)
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        for player in roomInfo['players']:
            TeamMessage(self.client, self.player).sendByID(player['plrID'])