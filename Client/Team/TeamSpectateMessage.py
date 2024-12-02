from Server.Team.TeamMessage import TeamMessage
from Utils.Reader import BSMessageReader
from Utils.G import Gameroom
import json
class TeamSpectateMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client 
    def decode(self):
    	#14358!!#
        self.roomHigh = self.read_Vint()
        self.room_id = self.read_Vint()
        self.roomType = self.read_Vint()
    def process(self):
        try:
            rooms = Gameroom()
            roomInfo = rooms.get_room_id(self.room_id)
            new_player = {"plrID":self.player.low_id,"STAT":self.player.online,"READY":False,"NAME":self.player.name,"OWNER":False}
            roomInfo['players'].append(new_player)
            self.player.room_id = self.room_id
            for player in roomInfo['players']:
                TeamMessage(self.client, self.player).sendByID(player['plrID'])
        except:
            pass