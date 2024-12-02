from Utils.Writer import Writer
from Utils.G import Gameroom
import json
class TeamStream2(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24131
        self.player = player

    def encode(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        premade_messages = roomInfo['premade']
        fm =[]
        if premade_messages:
            sorted_messages = sorted(premade_messages, key=lambda msg: msg['smstick'], reverse=True)
            latest_message = sorted_messages[0]  # Get the most recent message

            self.writeVint(0)
            self.writeVint(roomInfo['id'])
            self.writeVint(1)
            
            if latest_message['pin'] in fm:
                self.writeVint(6)
            else:
                self.writeVint(8)
                # StreamEntry::encode
                self.writeVint(0)
                self.writeVint(latest_message['smstick'])  # tick
                self.writeVint(0)
                self.writeVint(latest_message['id'])
                self.writeString(f"{latest_message['name']}")
                self.writeVint(0)
                self.writeVint(0)  # Age Seconds (TID_STREAM_ENTRY_AGE)
                self.writeVint(0)  # Boolean
                if latest_message['Type'] in fm:
                    self.writeScId(40, 0)
                if True:
                    self.writeScId(40, latest_message['Type'])  # Message Data ID (40 - messages.csv)
                    tbool = True if latest_message["Type"]!=46 else False
                    self.writeBoolean(tbool)  # Target Boolean
                    self.writeString(self.player.name)  # Target Name
                    self.writeVint(0)  # ??
                    self.writeVint(latest_message['pin'])