from Utils.Reader import BSMessageReader
from Server.Team.TeamMessage import TeamMessage
from Server.Team.TeamInvitationMessage import TeamInvitationMessage
from Utils.G import Gameroom

class TeamInviteMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
    def decode(self):
        self.read_Vint()#highID
        self.ID = self.read_Vint()#lowID
    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        new_player = {'id':self.ID,'state':0}
        roomInfo['invites'].append(new_player)
        TeamInvitationMessage(self.client, self.player)
        for player in roomInfo['players']:
            TeamMessage(self.client, self.player).sendWithLowID(player['plrID'])