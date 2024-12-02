from Utils.Reader import BSMessageReader
from Server.Team.TeamMessage import TeamMessage
from Server.Team.TeamStream import TeamStream 
from Utils.G import Gameroom

class TeamInvitationResponseMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
    def decode(self):
        self.Response = self.read_Vint();
        self.ID2 = self.read_int()#LOW_ID
        self.roomID = self.read_int()#LOW_ID
    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.roomID)
        if self.Response == 1:
            new_player = {"plrID":self.player.low_id,"STAT":self.player.online,"READY":False,"NAME":self.player.name,"OWNER":False}
            for invite in roomInfo['invites']:
                if invite['id'] == self.player.low_id:
                        roomInfo['invites'].remove(invite)
            roomInfo['players'].append(new_player)
            roomInfo['Tick'] += 1
            new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'name':self.player.name,'event':4,'type':102,'senderID':self.player.low_id,'senderN':self.player.name}
            roomInfo['msg'].append(new_msg)
            self.player.room_id = self.roomID
            for player in roomInfo['players']:
                TeamMessage(self.client, self.player).sendWithLowID(player['plrID'])
                TeamStream(self.client, self.player).sendWithLowID(player['plrID'])
        if self.Response == 2:
            for invite in roomInfo['invites']:
                if invite['id'] == self.player.low_id:
                    roomInfo['invites'].remove(invite)
            for player in roomInfo['players']:
                TeamMessage(self.client, self.player).sendWithLowID(player['plrID'])