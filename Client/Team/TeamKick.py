from Utils.Reader import BSMessageReader
from Server.Team.TeamMessage import TeamMessage
from Server.Team.TeamStream import TeamStream
from Server.Team.TeamLeaveOkMessage import TeamLeaveOkMessage
from Utils.G import Gameroom
from database.DataBase import DataBase

class TeamKick(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
    def decode(self):
        self.read_Vint()#highID
        self.ID = self.read_Vint()#lowID
        self.players = DataBase.loadbyID(self,self.ID)
    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        for player in roomInfo['players']:
            if player['plrID'] == self.ID:
                roomInfo['players'].remove(player)
        roomInfo['Tick'] += 1
        new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'name':self.players[2],'event':4,'type':104,'senderID':self.ID,'senderN':self.player.name}
        roomInfo['msg'].append(new_msg)
        for player in roomInfo['players']:
            TeamMessage(self.client, self.player).sendWithLowID(player['plrID'])
            TeamStream(self.client, self.player).sendWithLowID(player['plrID'])
        TeamLeaveOkMessage(self.client, self.player).sendWithLowID(self.ID)