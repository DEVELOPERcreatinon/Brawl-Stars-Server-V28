from Utils.Writer import Writer
from Utils.G import Gameroom

class TeamStream(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24131
        self.player = player

    def encode(self):
        rooms = Gameroom()
        roomInfo = rooms.get_room_id(self.player.room_id)
        premade_messages = roomInfo['msg']
        if premade_messages:
            sorted_messages = sorted(premade_messages, key=lambda msg: msg['smstick'], reverse=True)
            latest_message = sorted_messages[0]

            self.writeVint(0) # High ID
            self.writeVint(roomInfo['id']) # Room ID
            self.writeVint(1) # count
			
            self.writeVint(latest_message['event']) # Event? 
            self.writeVint(0)
            self.writeVint(latest_message['smstick']) # Tick? 
            self.writeVint(0)  # High ID
            self.writeVint(latest_message['id']) # Low id
            self.writeString(f"{latest_message['name']}") # Plr Name? 
            self.writeVint(0)
            self.writeVint(0) # Age Seconds (TID_STREAM_ENTRY_AGE)
            self.writeVint(0) # Boolean
            if latest_message['event'] == 4:
                self.writeVInt(latest_message['type'])#1 = Kicked, 2 = Join request accepted, 3 = Join the club, 4 = Leave the club
                self.writeVInt(1)
                self.writeVInt(0)
                self.writeVInt(latest_message['senderID'])
                self.writeString(f"{latest_message['senderN']}")
            else:
                self.writeString(f"{latest_message['msg']}") # Plr msg