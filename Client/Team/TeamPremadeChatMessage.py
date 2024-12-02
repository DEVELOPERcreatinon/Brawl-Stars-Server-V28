from Utils.Reader import BSMessageReader
from Server.Team.TeamStream2 import TeamStream2
from Server.Team.TeamMessage import TeamMessage
from Utils.G import Gameroom
class TeamPremadeChatMessage(BSMessageReader):
	def __init__(self, client, player, initial_bytes):
		super().__init__(initial_bytes)
		self.client = client
		self.player = player
        
	def decode(self):
		self.read_Vint()
		self.Type = self.read_Vint()
		self.read_Vint()
		self.read_Vint()
		self.pin = self.read_Vint()
		

	def process(self):
		roomInfo = Gameroom().get_room_id(self.player.room_id)
		roomInfo['Tick'] += 1
		new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'Type':self.Type,'pin':self.pin,'name':self.player.name,}
		roomInfo['premade'].append(new_msg)
		for player in roomInfo['players']:
			sendStream = TeamStream2(self.client, self.player)
			sendStream.sendByID(player['plrID'])
			TeamMessage(self.client, self.player).sendByID(player['plrID'])
        