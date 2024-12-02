from Server.Team.TeamMessage import TeamMessage
from Server.Team.TeamStream import TeamStream
from Utils.Reader import BSMessageReader
from Utils.G import Gameroom

class TeamCreateMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.mapSlot = self.read_Vint()
        self.map_id = self.read_Vint()
        self.roomType = self.read_Vint()

    def process(self):
        rooms = Gameroom()
        count = len(rooms.get_rooms()) + 1
        self.player.room_id = count
        rooms.create(count,self.map_id,self.roomType,self.player.low_id,self.player.brawler_id,self.player.skin_id,self.player.online,self.player.name)
        roomInfo = Gameroom().get_room_id(self.player.room_id)
        roomInfo['Tick'] += 1
        new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'name':self.player.name,'event':4,'type':101,'senderID':self.player.low_id,'senderN':self.player.name}
        roomInfo['msg'].append(new_msg)
        TeamMessage(self.client, self.player).send()
        for player in roomInfo['players']:
            TeamStream(self.client, self.player).sendWithLowID(player['plrID'])