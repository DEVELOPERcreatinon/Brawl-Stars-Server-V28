from Utils.Reader import BSMessageReader
from Server.Team.TeamStream import TeamStream
from Server.Team.TeamMessage import TeamMessage
from Utils.G import Gameroom

class TeamChat(BSMessageReader):
	#14369
	def __init__(self, client, player, initial_bytes):
		super().__init__(initial_bytes)
		self.client = client
		self.player = player
		
	def decode(self):
		self.message = self.read_string()
		 
	def process(self):
		roomInfo = Gameroom().get_room_id(self.player.room_id)
		roomInfo['Tick'] += 1
		new_msg = {'smstick':roomInfo['Tick'],'id':self.player.low_id,'name':self.player.name,'msg':self.message,'event':2}
		roomInfo['msg'].append(new_msg)
		for player in roomInfo['players']:
			sendStream = TeamStream(self.client, self.player)
			sendStream.sendByID(player['plrID'])
			TeamMessage(self.client, self.player).sendByID(player['plrID'])