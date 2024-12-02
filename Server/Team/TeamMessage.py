from Utils.Writer import Writer
from database.DataBase import DataBase
from Utils.G import Gameroom
from Utils.Helpers import Helpers
import json
from Server.Team.TeamInvitationMessage import TeamInvitationMessage

class TeamMessage(Writer):
    def __init__(self, client, player, roomType=1):
        super().__init__(client)
        self.id = 24124
        self.player = player
        self.playerCount = 0
        self.roomType = roomType
    def encode(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        self.writeVint(roomInfo['roomType'])
        self.writeVint(0)#max plr
        self.writeVint(1)

        self.writeInt(0)
        self.writeInt(roomInfo['id'])

        self.writeVint(1557129593)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
		
		
        self.writeScId(15, roomInfo['mapID'])# MapID
        #playe
        for plr in roomInfo['players']:
            self.writeVint(len(roomInfo['players']))#count plrs
            self.writeVint(plr['OWNER'])  # Boolean admin
            self.players = DataBase.loadbyID(self,plr['plrID'])
            self.writeInt(0)#hight_id
            self.writeInt(plr['plrID'])#low_id
            brawler=self.players[14]
            self.writeScId(16, self.players[14])#brawler
            self.writeScId(29, self.players[15])#skin
            brawlerData = json.loads(self.players[13])
            self.writeVint(int(brawlerData["brawlersTrophies"][str(brawler)])) # int(brawlerData["brawlersTrophies"][str(brawler)])
            self.writeVint(int(brawlerData["brawlersTrophies"][str(brawler)]))
            self.writeVint(int(brawlerData["brawlerPowerLevel"][str(brawler)])+1) # brawler level
            self.writeVint(plr['STAT']) #status
            self.writeVint(plr['READY']) # Is ready
            self.writeVint(0)
            self.writeVint(0)
            self.writeVint(0)
            if plr['plrID'] in config['vips']:
                self.writeString(f"{plr['NAME']}")
            else:
                self.writeString(f"{plr['NAME']}")
            self.writeVint(100)
            self.writeVint(28000000 + self.players[9])
            self.writeVint(43000000 + self.players[10])
            if plr['plrID'] in config['vips']:
                self.writeVint(43000000 + self.players[10])
            else:
                self.writeVint(0)

            self.writeVint(0)#sps
            self.writeVint(0)#spg
			
        self.writeVint(len(roomInfo['invites']))
        for data in roomInfo['invites']:
            if data['state'] == 0:
                TeamInvitationMessage(self.client, self.player, self.player.room_id, self.player.low_id).sendWithLowID(data['id'])
                self.writeVint(1)
                self.writeVint(1)
                self.writeInt(0)
                self.writeInt(self.player.room_id)
                self.writeInt(0)
                self.writeInt(data['id'])#low_id
                self.invtitesload = DataBase.loadbyID(self,data['id'])
                if data['id'] in config['vips']:
                    self.writeString(f"{self.invtitesload[2]}")
                else:
                    self.writeString(f"{self.invtitesload[2]}")
                self.writeVint(1)#1
                self.writeVint(len(roomInfo['invites']))#slot

        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)