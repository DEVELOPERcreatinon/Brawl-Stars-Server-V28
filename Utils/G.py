import json

class Gameroom:
    rooms = []
    def get_rooms(self):
        return self.rooms
    def create(self,roomID=1,mapID=7,roomType=1,ID=2,BID=0,SID=52,STAT=2,NAME=233):
        new_player = {"plrID":ID,"STAT":STAT,"READY":False,"NAME":NAME,"OWNER":True}
        new_rooms = {
			"id": roomID,
			"mapID": mapID,
			"roomType": roomType,
			"Tick": 1,
			"premade": [],
			"msg": [],
			"invites": [],
			"players": [new_player]
        }
        self.rooms.append(new_rooms)
    def get_room_id(self, roomID):
        for room in self.rooms:
            if room["id"] == roomID:
                return room
        return None