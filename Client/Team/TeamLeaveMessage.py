from Server.Team.TeamLeaveOkMessage import TeamLeaveOkMessage
from Server.Team.TeamMessage import TeamMessage
from Server.Team.TeamStream import TeamStream
from Utils.G import Gameroom
from Utils.Reader import BSMessageReader


class TeamLeaveMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        pass

    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        for player in roomInfo['players']:
            if player['plrID'] == self.player.low_id:
                roomInfo['players'].remove(player)
        roomInfo['Tick'] += 1
        new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'name':self.player.name,'event':4,'type':103,'senderID':self.player.low_id,'senderN':self.player.name}
        roomInfo['msg'].append(new_msg)
        for player in roomInfo['players']:
            TeamMessage(self.client, self.player).sendWithLowID(player['plrID'])
            TeamStream(self.client, self.player).sendWithLowID(player['plrID'])
        TeamLeaveOkMessage(self.client, self.player).send() 