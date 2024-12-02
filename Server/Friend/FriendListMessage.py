import sqlite3
import json
from Utils.Writer import Writer
from Server.Friend.FriendOnlineStatusEntryMessage import FriendOnlineStatusEntryMessage
from database.DataBase import DataBase
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class FriendListMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 20105
        self.player = player

    def encode(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('database/Player/plr.db')
            cursor = conn.cursor()

            # Fetch user data
            cursor.execute('SELECT * FROM plrs WHERE lowID=?', (self.player.low_id,))
            user = cursor.fetchone()

            if user is None:
                logger.warning(f"User with lowID {self.player.low_id} not found.")
                return

            # Load friends data
            friends_json = user[22]
            friends = json.loads(friends_json)

            self.writeInt(0)
            self.writeBoolean(True)
            self.writeInt(len(friends))

            for data in friends:
                # Fetch player data by ID
                self.players = DataBase.loadbyID(self, data["id"])

                if self.players is None:
                    logger.warning(f"Player with ID {data['id']} not found.")
                    continue  # Skip this friend if player data is not found

                # Write friend data
                self.writeInt(0)  # HighID
                self.writeInt(self.players[1])  # LowID

                self.writeString('')
                self.writeString('')
                self.writeString('')
                self.writeString('')
                self.writeString('')
                self.writeString('')

                self.writeInt(self.players[3])  # Trophies
                self.writeInt(data["state"])
                self.writeInt(0)
                self.writeInt(0)
                self.writeInt(0)

                self.writeBoolean(False)

                self.writeString('')
                self.writeInt(0)

                self.writeBoolean(True)  # Is a player?

                # Write player name
                if self.players[20] == 1:
                    self.writeString(f"{self.players[2]}") 
                else:
                    self.writeString(f"{self.players[2]}")
                
                # Write additional data
                self.writeVint(100)
                self.writeVint(28000000 + self.players[9])
                self.writeVint(43000000 + self.players[10])
                if self.players[20] == 1:
                    self.writeVint(43000000 + self.players[10])  # Name color
                else:
                    self.writeVint(0)  # Name color

                # Send online status message
                FriendOnlineStatusEntryMessage(self.client, self.player, data["id"], self.players[19], self.players[16]).send()

        except Exception as e:
            logger.error(f"Error encoding FriendListMessage: {e}")
        finally:
            conn.close()