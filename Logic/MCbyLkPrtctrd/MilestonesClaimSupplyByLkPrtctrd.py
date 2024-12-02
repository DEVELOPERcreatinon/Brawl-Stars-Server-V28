from Utils.Writer import Writer
from random import randint as r
from database.DataBase import DataBase
from Logic.MCbyLkPrtctrd.MilestonesClaimHelpByLkPrtctrd import MilestonesClaimHelpByLkPrtctrd as Lyney 
import random as rnd
from Logic.Commands.Client.LogicBoxDataCommand import LogicBoxDataCommand as BOXES

class MilestonesClaimSupplyByLkPrtctrd(Writer):

    MAX_BRAWLER_POINTS = 1410  # New limit for upgrade points
    EXCLUDED_BRAWLER_ID = [0, 1, 2, 3, 7, 8, 9, 14, 22, 27, 30]  # Define the IDs of the brawlers to exclude

    def __init__(self, client, player, what, data):
        super().__init__(client)
        self.id = 24111
        self.player = player
        self.id1 = what
        self.mult1 = data

    def encode(self):
        self.writeBool = self.writeBoolean
        self.writeVInt = self.writeVint

        if self.id1 == "BOXLkPrtctrd":
            boxtype = self.mult1["BoxDID"]
            money = Lyney().GetAmountOfBox(boxtype)
            moneygive = [money]
            try:
                del self.player.UnlockedBrawlers["48"]
            except KeyError:
                pass

            ownedbrs = [int(LkPrtctrd) for LkPrtctrd, x in self.player.UnlockedBrawlers.items() if int(x) == 1 and int(LkPrtctrd) < 39 and self.player.brawlerPoints.get(str(LkPrtctrd), 0) < self.MAX_BRAWLER_POINTS]
            ownedbrsforall = [int(LkPrtctrd) for LkPrtctrd, x in self.player.UnlockedBrawlers.items() if int(x) == 1 and int(LkPrtctrd) < 39]
            allbrswithoutown = [int(LkPrtctrd) for LkPrtctrd in range(39) if LkPrtctrd not in ownedbrsforall and LkPrtctrd != 33 and LkPrtctrd != 48]

            if boxtype == 11:
                ppcount = min(5, len(ownedbrs))
            elif boxtype == 10:
                ppcount = min(2, len(ownedbrs))
            else:
                ppcount = min(3, len(ownedbrs))

            powerpointsgive = []
            pointsgivetable = {
                "10": {"1": 10, "2": 25},
                "11": {"1": 80, "2": 200},
                "12": {"1": 30, "2": 75}
            }
            for _ in range(ppcount):
                if not ownedbrs:
                    break
                brawler = rnd.choice(ownedbrs)
                pointsnow = self.player.brawlerPoints.get(str(brawler), 0)
                pointsgive = rnd.randint(pointsgivetable[str(boxtype)]["1"], pointsgivetable[str(boxtype)]["2"])
                pointsgivefinish = min(pointsgive, self.MAX_BRAWLER_POINTS - pointsnow)
                ownedbrs.remove(brawler)
                if pointsgivefinish > 0:
                    if self.player.brawlerPowerLevel.get(str(brawler), 0) < 9:
                        powerpointsgive.append({"Brawler": brawler, "Points": pointsgivefinish})

            # Probabilities for brawlers
            brawler_probabilities = {
                6: 5,  # барди
                10: 5,
                13: 5,
                24: 5,  # редкие
                19: 4,
                18: 4,
                25: 4,
                34: 4,  # сверхредкие
                15: 3,
                16: 3,
                20: 3,
                26: 3,
                30: 3,  # эпики
                36: 2,
                11: 2,
                17: 2,
                21: 2,
                37: 2,
                31: 2,
                32: 2,
                35: 2,  # хромики
                38: 2,
                5: 1,  # легендарки
                12: 1,
                23: 1,
            }

            brawler_list = list(brawler_probabilities.keys())
            brawler_weights = list(brawler_probabilities.values())
            
            # Initialize brsgivecount with a chance of 10% for each brawler
            brsgivecount = 5  # Default count or adjust based on requirements

            brsgive = []
            for _ in range(brsgivecount):
                if not allbrswithoutown:
                    break
                # 10% chance to add a brawler to the list
                if rnd.random() < 0.10:
                    brawler = rnd.choices(brawler_list, weights=brawler_weights, k=1)[0]
                    if brawler in allbrswithoutown and brawler not in self.EXCLUDED_BRAWLER_ID:
                        allbrswithoutown.remove(brawler)
                        brsgive.append(brawler)

            if boxtype == 10 and brsgive:
                powerpointsgive = []
                moneygive = []

            self.writeVint(203)
            self.writeVint(0)
            self.writeVint(1)
            self.writeVint(boxtype)

            rewardcount = len(moneygive) + len(powerpointsgive) + len(brsgive)
            self.writeVint(rewardcount)
            for x in moneygive:
                self.writeVint(x)
                self.writeBPScId(0, 0)
                self.writeVint(7)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
            for x in powerpointsgive:
                self.writeVint(x["Points"])
                self.writeBPScId(16, x["Brawler"])
                self.writeVint(6)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
            for x in brsgive:
                self.writeVint(1)
                self.writeBPScId(16, x)
                self.writeVint(1)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)

            self.writeBool(False)
            try:
                self.writeVint(self.mult1["Road"])
                self.writeVint(self.mult1["Level"] + 2)
                self.writeVint(self.mult1["Season"])
            except KeyError:
                self.writeVint(0)
                self.writeVint(0)
                self.writeVint(0)

            for _ in range(11):
                self.writeVInt(0)

            for x in moneygive:
                self.player.gold += x
                DataBase.replaceValue(self, 'gold', self.player.gold)
            for x in powerpointsgive:
                if self.player.brawlerPowerLevel.get(str(x["Brawler"]), 0) < 9:
                    self.player.brawlerPoints[str(x["Brawler"])] = min(self.player.brawlerPoints.get(str(x["Brawler"]), 0) + x["Points"], self.MAX_BRAWLER_POINTS)
                    DataBase.replaceValue(self, 'brawlerPoints', self.player.brawlerPoints)
            for x in brsgive:
                self.player.UnlockedBrawlers[str(x)] = 1
                DataBase.replaceValue(self, 'UnlockedBrawlers', self.player.UnlockedBrawlers)
            return

        if self.id1 == "BPLkPrtctrd":
            self.writeVint(203)
            self.writeVint(0)
            self.writeVint(1)
            try:
                self.writeVint(self.mult1["Box"])
            except KeyError:
                self.writeVint(100)

            if self.mult1["Type"] == 6:
                brawler = self.mult1["Character"][1]
                resbeen = self.player.brawlerPoints.get(str(brawler), 0)
                if resbeen + self.mult1["Amount"] > self.MAX_BRAWLER_POINTS:
                    resnewplus = self.MAX_BRAWLER_POINTS - resbeen
                    resnewmoney = self.mult1["Amount"] - resnewplus
                else:
                    resnewplus = self.mult1["Amount"]
                    resnewmoney = 0
                resnewpp = [resnewplus, resnewmoney * 2]

            rewardcount = 1
            if self.mult1["Type"] == 6:
                rewardcount = 2 if resnewpp[1] > 0 else 1
            elif self.mult1["Type"] == 9:
                rewardcount = 2 if self.player.UnlockedBrawlers.get(str(self.mult1['Character'][1]), 0) == 0 else 1

            self.writeVint(rewardcount)
            if self.mult1["Type"] not in [1, 6, 9]:
                self.writeVint(self.mult1["Amount"])
                self.writeBPScId(0, 0)
                self.writeVint(self.mult1["Type"])
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
            elif self.mult1["Type"] == 1:
                self.writeVint(self.mult1["Amount"])
                self.writeBPScId(16, self.mult1["Character"][1])
                self.writeVint(self.mult1["Type"])
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
            elif self.mult1["Type"] == 9:
                if rewardcount == 2:
                    self.writeVint(1)
                    self.writeBPScId(16, self.mult1["Character"][1])
                    self.writeVint(1)
                    self.writeBPScId(0, 0)
                    self.writeBPScId(0, 0)
                    self.writeBPScId(0, 0)
                    self.writeVint(0)
                    self.player.UnlockedBrawlers[str(self.mult1["Character"][1])] = 1
                    DataBase.replaceValue(self, 'UnlockedBrawlers', self.player.UnlockedBrawlers)
                self.writeVint(1)
                self.writeBPScId(16, self.mult1["Character"][1])
                self.writeVint(9)
                self.writeBPScId(29, self.mult1["Skin"][1])
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
            elif self.mult1["Type"] == 6:
                self.writeVint(resnewpp[0])
                self.writeBPScId(16, self.mult1["Character"][1])
                self.writeVint(6)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeBPScId(0, 0)
                self.writeVint(0)
                if resnewpp[1] > 0:
                    self.writeVint(resnewpp[1])
                    self.writeBPScId(0, 0)
                    self.writeVint(7)
                    self.writeBPScId(0, 0)
                    self.writeBPScId(0, 0)
                    self.writeBPScId(0, 0)
                    self.writeVint(0)
            self.writeBoolean(False)
            self.writeVint(self.mult1["Road"])
            self.writeVint(self.mult1["Level"] + 2)
            self.writeVint(self.mult1["Season"])
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)
            self.writeVInt(0)

            if self.mult1["Type"] == 7:
                self.player.gold += self.mult1['Amount']
                DataBase.replaceValue(self, 'gold', self.player.gold)
            elif self.mult1["Type"] == 8:
                self.player.gems += self.mult1['Amount']
                DataBase.replaceValue(self, 'gems', self.player.gems)
            elif self.mult1["Type"] == 6:
                self.player.gold += resnewpp[1]
                DataBase.replaceValue(self, 'gold', self.player.gold)
                if self.player.brawlerPowerLevel.get(str(self.mult1["Character"][1]), 0) < 9:
                    self.player.brawlerPoints[str(self.mult1["Character"][1])] = min(self.player.brawlerPoints.get(str(self.mult1["Character"][1]), 0) + resnewpp[0], self.MAX_BRAWLER_POINTS)
                    DataBase.replaceValue(self, 'brawlerPoints', self.player.brawlerPoints)
            elif self.mult1["Type"] == 1:
                self.player.UnlockedBrawlers[str(self.mult1["Character"][1])] = 1
                DataBase.replaceValue(self, 'UnlockedBrawlers', self.player.UnlockedBrawlers)
            elif self.mult1["Type"] == 9:
                self.player.UnlockedSkins[str(self.mult1["Skin"][1])] = 1
                DataBase.replaceValue(self, 'UnlockedSkins', self.player.UnlockedSkins)
            return