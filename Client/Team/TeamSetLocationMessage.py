from Server.Team.TeamMessage import TeamMessage
from Utils.Reader import BSMessageReader
from Utils.G import Gameroom
import json

class TeamSetLocationMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client 

    def decode(self):
        self.read_Vint()
        self.mapa = self.read_Vint()

    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        roomInfo['mapID'] = self.mapa
        for player in roomInfo['players']:
            TeamMessage(self.client, self.player).sendByID(player['plrID'])