from database.DataBase import DataBase
from Utils.Reader import BSMessageReader
from Utils.Writer import Writer
import sqlite3
import json

class FriendSuggestionsMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
    def decode(self):
        self.HighID = self.read_int()
        self.LowID = self.read_int()
    def process(self):
        sendStream = AddableFriendsMessage(self.client, self.player)
        sendStream.send()

class AddableFriendsMessage(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.id = 20199
        self.player = player

    def encode(self):
        db = DataBase.getSuggestions(self)
        friends = []
        if self.player.low_id > 2:
            conn = sqlite3.connect('database/Player/plr.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM plrs WHERE lowID=?', (self.player.low_id,))
            user = cursor.fetchone()
            friends_json = user[22]
            friends = json.loads(friends_json)
        filtered_db = []

        for data in db:
            if data[0] not in [friend['id'] for friend in friends] and data[0] != self.player.low_id:
                filtered_db.append(data)

        self.writeInt(len(friends))
        for data in friends:
            self.players = DataBase.loadbyID(self,  data["id"])
            self.writeInt(0)  # HighID
            self.writeInt(self.players[1])  # LowID

            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()
            self.writeString()

            self.writeInt(self.players[3])  # Trophies
            self.writeInt(data["state"])
            self.writeInt(0)
            self.writeInt(0)
            self.writeInt(0)

            self.writeBoolean(False)

            self.writeString()
            self.writeInt(0)

            self.writeBoolean(True)  # ?? is a player?
		
            if self.players[20] == 1:
                self.writeString(f"{self.players[2]} - VIP") 
            else:
                self.writeString(f"{self.players[2]}")
            self.writeVint(100)
            self.writeVint(28000000 + self.players[9])
            self.writeVint(43000000 + self.players[10])
            if self.players[20] == 1:
                self.writeVint(43000000 + self.players[10])  # Name color
            else:
	            self.writeVint(0)  # Name color