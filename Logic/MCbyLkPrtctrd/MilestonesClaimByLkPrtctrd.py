from database.DataBase import DataBase
#from Cmd.LogicBoxDataCommand import LogicBoxDataCommand
from Utils.Reader import BSMessageReader
from Logic.MCbyLkPrtctrd.MilestonesClaimHelpByLkPrtctrd import MilestonesClaimHelpByLkPrtctrd as Help
from Logic.MCbyLkPrtctrd.MilestonesClaimSupplyByLkPrtctrd import MilestonesClaimSupplyByLkPrtctrd as Supply
import random as rnd
class MilestonesClaimByLkPrtctrd(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.read_Vint() #мда
        self.read_Vint() #мда
        self.read_Vint() #мда
        self.read_Vint() #мда

        self.Road = self.read_Vint()
        if self.read_Vint() == 16:
            self.Character = [16, self.read_Vint()]
        self.Season = self.read_Vint()
        self.Level = self.read_Vint()

    def process(self):
        if self.Road==10:
            if self.Season in [1]:
                if self.Level in [2,14,22,36,44,52,62]:
                    amount = 20 if self.Level in [22,62] else 10
                    Supply(self.client, self.player, "BPLkPrtctrd", {"Type":8,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [6,18,32,48,56,67]:
                    amount = Help().GetAmountOfLevel(self.Level, [6,18,32,48,56,67], [50,50,100,200,200,500])
                    Supply(self.client, self.player, "BPLkPrtctrd", {"Type":7,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [1,4,8,12,16,21,24,28,33,38,41,43,46,54,58,63]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 10, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [0,3,5,7,9,11,13,15,17,19,23,25,27,29,31,35,37,39,47,49,53,57,59,61,66,68]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [10,20,30,40,45,51,55,60,65,69]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 11, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [26,34,42,50,64,70]:
                    try:
                        self.Character
                        amount = Help().GetAmountOfLevel(self.Level, [26,34,42,50,64,70], [50,50,75,100,100,500])
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character, "Type":6,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    except:
                        boxalternate = Help().GetAmountOfLevel(self.Level, [26,34,42,50,64,70], [10,10,10,12,12,11])
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": boxalternate, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
        elif self.Road==9:
            if self.Season in [1]:
                if self.Level in [2,4,8,10,14,23,34,46]:
                    amount = Help().GetAmountOfLevel(self.Level+1, [3,5,9,11,15,24,35,47], [100,100,100,100,200,200,200,300])
                    Supply(self.client, self.player, "BPLkPrtctrd", {"Type":7,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [3,7,11,13,17,20,25,26,31,32,36,40,44]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [1,9,19,29,42]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 11, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [5]:
                    boxalternate = 12
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": boxalternate, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [15]:
                    brawler = Help().GetAmountOfLevel(self.Season+1, [2], [38])
                    if self.player.UnlockedBrawlers[str(brawler)]==0:
                        amount = 1
                        self.Character = [16,brawler]
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character,"Type":1,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    else:
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [0]:
                    brawler = Help().GetAmountOfLevel(self.Season+1, [2], [3])
                    skin = Help().GetAmountOfLevel(self.Season+1, [2], [201])
                    if self.player.UnlockedSkins[str(skin)] == 0:
                        amount = 1
                        self.Skin = [29,skin]
                        self.Character = [16,brawler]
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character, "Skin": self.Skin,"Type":9,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    else:
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [50]:
                    brawler = Help().GetAmountOfLevel(self.Season+1, [2], [38])
                    skin = Help().GetAmountOfLevel(self.Season+1, [2], [203])
                    if self.player.UnlockedSkins[str(skin)] == 0:
                        amount = 1
                        self.Skin = [29,skin]
                        self.Character = [16,brawler]
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character, "Skin": self.Skin,"Type":9,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    else:
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [6,12,22,28,38,48]:
                    try:
                        self.Character
                        amount = Help().GetAmountOfLevel(self.Level, [6,12,22,28,38,48], [50,100,100,200,200,500])
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character, "Type":6,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    except:
                        boxalternate = Help().GetAmountOfLevel(self.Level, [6,12,22,28,38,48], [10,12,12,12,12,11])
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": boxalternate, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [16,18,21,24,27,30,33,35,37,39,41,43,45,47,49]:
                    boxalternate = 10
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": boxalternate, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()

        elif self.Road == 6:
            snap = self.player.Troproad-1==self.Level
            if snap:
                if self.Level in [0, 2, 4, 13, 19, 26, 36, 39, 41, 48, 51, 61]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 10, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [17, 23, 30, 32, 57, 66, 72, 75, 77, 83, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 12, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [59, 69, 79, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164]:
                    Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 11, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [1, 5, 9, 14, 24, 34, 44, 54, 64, 74]:
                    brawler = Help().GetAmountOfLevel(self.Level, [1, 5, 9, 14, 24, 34, 44, 54, 64, 74], [8,1,2,7,3,9,14,22,27,30])
                    if self.player.UnlockedBrawlers[str(brawler)]==0:
                        amount = 1
                        self.Character = [16,brawler]
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character,"Type":1,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    else:
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": 10, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [6,50]:
                    amount = Help().GetAmountOfLevel(self.Level, [6,50], [200,600])
                    Supply(self.client, self.player, "BPLkPrtctrd", {"Type":7,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [15, 18, 22, 25, 28, 31, 35, 38, 40, 43, 45, 47, 49, 53, 56, 62, 65, 68, 70, 73, 78, 80, 82, 85, 89, 93]:
                    amount = Help().GetAmountOfLevel(self.Level, [15, 18, 22, 25, 28, 31, 35, 38, 40, 43, 45, 47, 49, 53, 56, 62, 65, 68, 70, 73, 78, 80, 82, 85, 89, 93], [50, 50, 50, 50, 100, 50, 50, 50, 150, 50, 50, 300, 50, 50, 200, 150, 200, 200, 50, 50, 200, 150, 150, 500, 500, 1000])
                    Supply(self.client, self.player, "BPLkPrtctrd", {"Type":7,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                elif self.Level in [8, 12, 16, 21, 27, 29, 33, 37, 42, 46, 52, 55, 58, 60, 63, 67, 71, 76, 81, 87, 91]:
                    try:
                        self.Character
                        amount = Help().GetAmountOfLevel(self.Level, [8, 12, 16, 21, 27, 29, 33, 37, 42, 46, 52, 55, 58, 60, 63, 67, 71, 76, 81, 87, 91], [25, 25, 25, 25, 75, 50, 50, 150, 25, 25, 25, 150, 25, 25, 25, 150, 25, 150, 50, 200, 100])
                        Supply(self.client, self.player, "BPLkPrtctrd", {"Character": self.Character, "Type":6,"Amount": amount, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                    except:
                        boxalternate = Help().GetAmountOfLevel(self.Level, [8, 12, 16, 21, 27, 29, 33, 37, 42, 46, 52, 55, 58, 60, 63, 67, 71, 76, 81, 87, 91], [10, 10, 10, 10, 10, 10, 10, 12, 10, 10, 10, 12, 10, 10, 10, 12, 10, 12, 10, 12, 12])
                        Supply(self.client, self.player, "BOXLkPrtctrd", {"BoxDID": boxalternate, "Road": self.Road, "Season": self.Season, "Level": self.Level}).send()
                else:
                    pass
            else:
                return

        else:
            print(f"Unknown milestone type: {self.Road}")
        
        if self.Road in [6]:
            self.player.Troproad = self.Level+2
            DataBase.replaceValue(self,'Troproad', self.player.Troproad)
        import json
        if self.Road in [9] and self.Season in [1]:
            try:
                self.player.buypass = json.loads(self.player.buypass)
            except:
                self.player.buypass
            self.player.buypass.append(self.Level)
            self.player.buypass = json.dumps(self.player.buypass)
            DataBase.replaceValue(self,'buypass', self.player.buypass)
        if self.Road in [10] and self.Season in [1]:
            try:
                self.player.freepass = json.loads(self.player.freepass)
            except:
                self.player.freepass
            self.player.freepass.append(self.Level)
            self.player.freepass = json.dumps(self.player.freepass)
            DataBase.replaceValue(self,'freepass', self.player.freepass)
        