from Server.Team.TeamMessage import TeamMessage
from Utils.Reader import BSMessageReader
from Utils.G import Gameroom

class TeamMemberStatusMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.state = self.read_Vint()
        self.player.pin = self.read_Vint()
        self.player.mode = self.read_Vint()

    def process(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        if roomInfo and 'players' in roomInfo:
            for player in roomInfo['players']:
                if player['plrID'] == self.player.low_id:
                    player['STAT'] = self.state
            for player in roomInfo['players']:
                TeamMessage(self.client, self.player).sendByID(player['plrID'])
        else:
            print(f"Игроков нету в руме: {self.player.room_id}")
