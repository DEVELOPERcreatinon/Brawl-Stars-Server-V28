from Utils.Writer import Writer
from database.DataBase import DataBase
import random
class BattleResultMessage(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.id = 23456
        self.player = player

    def encode(self):
        brawler_trophies = self.player.brawlers_trophies[str(self.player.brawler_id)]
        tropGainded = 0
        tokenGained = 0
		
        if 0 <= brawler_trophies <= 49:
            rank_1_val = 10
            rank_2_val = 8
            rank_3_val = 6
            rank_4_val = 4
            rank_5_val = 2
            rank_6_val = 0
            rank_7_val = 0
            rank_8_val = 0
            rank_9_val = 0
            rank_10_val = 0
        elif 50 <= brawler_trophies <= 99:
            rank_1_val = 10
            rank_2_val = 8
            rank_3_val = 6
            rank_4_val = 4
            rank_5_val = 2
            rank_6_val = -1
            rank_7_val = -2
            rank_8_val = -2
            rank_9_val = -3
            rank_10_val = -3
        elif 100 <= brawler_trophies <= 249:
            rank_1_val = 10
            rank_2_val = 8
            rank_3_val = 6
            rank_4_val = 3
            rank_5_val = 1
            rank_6_val = -2
            rank_7_val = -2
            rank_8_val = -3
            rank_9_val = -3
            rank_10_val = -4
        elif 250 <= brawler_trophies <= 399:
            rank_1_val = 10
            rank_2_val = 8
            rank_3_val = 4
            rank_4_val = 3
            rank_5_val = 0
            rank_6_val = -3
            rank_7_val = -3
            rank_8_val = -4
            rank_9_val = -4
            rank_10_val = -5
        elif 400 <= brawler_trophies <= 499:
            rank_1_val = 9
            rank_2_val = 8
            rank_3_val = 3
            rank_4_val = 1
            rank_5_val = -1
            rank_6_val = -3
            rank_7_val = -4
            rank_8_val = -4
            rank_9_val = -5
            rank_10_val = -5
        elif 500 <= brawler_trophies <= 649:
            rank_1_val = 8
            rank_2_val = 7
            rank_3_val = 3
            rank_4_val = 0
            rank_5_val = -2
            rank_6_val = -4
            rank_7_val = -5
            rank_8_val = -5
            rank_9_val = -5
            rank_10_val = -6
        elif 650 <= brawler_trophies <= 799:
            rank_1_val = 7
            rank_2_val = 6
            rank_3_val = 3
            rank_4_val = -2
            rank_5_val = -3
            rank_6_val = -5
            rank_7_val = -6
            rank_8_val = -6
            rank_9_val = -6
            rank_10_val = -7
        elif 800 <= brawler_trophies <= 899:
            rank_1_val = 6
            rank_2_val = 5
            rank_3_val = 2
            rank_4_val = -3
            rank_5_val = -4
            rank_6_val = -5
            rank_7_val = -6
            rank_8_val = -7
            rank_9_val = -7
            rank_10_val = -8
        elif 900 <= brawler_trophies <= 1000:
            rank_1_val = 5
            rank_2_val = 3
            rank_3_val = 1
            rank_4_val = -3
            rank_5_val = -4
            rank_6_val = -5
            rank_7_val = -6
            rank_8_val = -7
            rank_9_val = -7
            rank_10_val = -8
        elif 1100 <= brawler_trophies <= 1250:
            rank_1_val = 4
            rank_2_val = 2
            rank_3_val = -3
            rank_4_val = -4
            rank_5_val = -5
            rank_6_val = -6
            rank_7_val = -7
            rank_8_val = -7
            rank_9_val = -8
            rank_10_val = -9
        elif brawler_trophies >= 1250:
            rank_1_val = 4
            rank_2_val = 1
            rank_3_val = -4
            rank_4_val = -5
            rank_5_val = -6
            rank_6_val = -7
            rank_7_val = -8
            rank_8_val = -9
            rank_9_val = -10
            rank_10_val = -11
            pass
        
        if self.player.rank == 1:
            tropGainded = rank_1_val
            tokenGained = 20
        elif self.player.rank == 2:
            tropGainded = rank_2_val
            tokenGained = 20
        elif self.player.rank == 3:
            tropGainded = rank_3_val
            tokenGained = 20
        elif self.player.rank == 4:
            tropGainded = rank_4_val
            tokenGained = 15
        elif self.player.rank == 5:
            tropGainded = rank_5_val
            tokenGained = 15
        elif self.player.rank == 6:
            tropGainded = rank_6_val
            tokenGained = 15
        elif self.player.rank == 7:
            tropGainded = rank_7_val
            tokenGained = random.randint(10,15)
        elif self.player.rank == 8:
            tropGainded = rank_8_val
            tokenGained = random.randint(10,15)
        elif self.player.rank == 9:
            tropGainded = rank_9_val
            tokenGained = random.randint(1,10)
        elif self.player.rank == 10:
            tropGainded = rank_10_val
            tokenGained = random.randint(1,10)
        self.writeVint(2) # Battle End Game Mode 
        self.writeVint(self.player.rank) # Result 
        self.writeVint(tokenGained) # Tokens Gained
        if tropGainded >= 0:
            if self.player.vip == 1:
                tropGainded += 15
                self.writeVint(tropGainded) # Trophies Result
            else:
                self.writeVint(tropGainded) # Trophies Result
        if tropGainded < 0:
            self.writeVint(tropGainded) # Trophies Result
        self.writeVint(0) # Unknown (Power Play Related)
        if self.player.vip == 1:
            self.writeVint(125) # Doubled Tokens
            tokenGained += 125
        else:
            self.writeVint(0) # Doubled Tokens
        self.writeVint(0) # Double Token Event
        self.writeVint(0) # Token Doubler Remaining
        self.writeVint(0) # Big Game/Robo Rumble Time
        self.writeVint(0) # Unknown (Championship Related)
        self.writeVint(0) # Championship Level Passed
        self.writeVint(0) # Challenge Reward Type (0 = Star Points, 1 = Star Tokens)
        self.writeVint(0) # Challenge Reward Ammount
        self.writeVint(0) # Championship Losses Left
        self.writeVint(0) # Championship Maximun Losses
        self.writeVint(0) # Coin Shower Event
        if tropGainded > 0:
            if self.player.vip == 1:
                self.writeVint(15) # Underdog Trophies
            else:
                self.writeVint(0) # Underdog Trophies
        else:
            self.writeVint(0) # Underdog Trophies
        self.writeVint(16)# 48-спектатор 32-дружеская 16-обычная победа (-16) - повер плей
        self.writeVint(-64) # Championship Challenge Type
        self.writeVint(0) # Championship Cleared and Beta Quests
            
        # Players Array
        self.writeVint(6) # Battle End Screen Players
        
        self.writeVint(1) # Team and Star Player Type
        self.writeScId(16, self.player.brawler_id) # Player Brawler
        self.writeScId(29, self.player.skin_id) # Player Skin
        self.writeVint(self.player.brawlers_trophies[str(self.player.brawler_id)]) # Your Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(self.player.brawlerPowerLevel[str(self.player.brawler_id)]) # Your Brawler Power Level
        self.writeBoolean(True) # HighID and LowID Array
        self.writeInt(0) # HighID
        self.writeInt(self.player.low_id) # LowID
        self.writeString(self.player.name) # Your Name
        self.writeVint(100) # Player Experience Level
        self.writeVint(28000000 + self.player.profile_icon) # Player Profile Icon
        self.writeVint(43000000 + self.player.name_color) # Player Name Color
        if self.player.vip == 1:
            self.writeVint(43000000 + self.player.name_color) # Player Name Color
        else:
            self.writeVint(0) # Player Name Color

        self.writeVint(0) # Team and Star Player Type
        self.writeScId(16, self.player.bot1) # Bot 1 Brawler
        self.writeVint(0) # Bot 1 Skin
        self.writeVint(0) # Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(1) # Brawler Power Level
        self.writeBoolean(False) # HighID and LowID Array
        self.writeString(self.player.bot1_n) # Bot 1 Name
        self.writeVint(0) # Player Experience Level
        self.writeVint(28000000) # Player Profile Icon
        self.writeVint(43000000) # Player Name Color
        self.writeVint(43000000) # Player Name Color
            
        self.writeVint(0) # Team and Star Player Type
        self.writeScId(16, self.player.bot2) # Bot 2 Brawler
        self.writeVint(0) # Bot 2 Skin
        self.writeVint(0) # Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(1) # Brawler Power Level
        self.writeBoolean(False) # HighID and LowID Array
        self.writeString(self.player.bot2_n) # Bot 2 Name
        self.writeVint(0) # Player Experience Level
        self.writeVint(28000000) # Player Profile Icon
        self.writeVint(43000000) # Player Name Color
        self.writeVint(43000000) # Player Name Color

        self.writeVint(2) # Team and Star Player Type
        self.writeScId(16, self.player.bot3) # Bot 3 Brawler
        self.writeVint(0) # Bot 3 Skin
        self.writeVint(0) # Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(1) # Brawler Power Level
        self.writeBoolean(False) # HighID and LowID Array
        self.writeString(self.player.bot3_n) # Bot 3 Name
        self.writeVint(0) # Player Experience Level
        self.writeVint(28000000) # Player Profile Icon
        self.writeVint(43000000) # Player Name Color
        self.writeVint(43000000) # Player Name Color

        self.writeVint(2) # Team and Star Player Type
        self.writeScId(16, self.player.bot4) # Bot 4 Brawler
        self.writeVint(0) # Bot 4 Skin
        self.writeVint(0) # Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(1) # Brawler Power Level
        self.writeBoolean(False) # HighID and LowID Array
        self.writeString(self.player.bot4_n) # Bot 4 Name
        self.writeVint(0) # Player Experience Level
        self.writeVint(28000000) # Player Profile Icon
        self.writeVint(43000000) # Player Name Color
        self.writeVint(43000000) # Player Name Color

        self.writeVint(2) # Team and Star Player Type
        self.writeScId(16, self.player.bot5) # Bot 5 Brawler
        self.writeVint(0) # Bot 5 Skin
        self.writeVint(0) # Brawler Trophies
        self.writeVint(0) # Unknown (Power Play Related)
        self.writeVint(1) # Brawler Power Level
        self.writeBoolean(False) # HighID and LowID Array
        self.writeString(self.player.bot5_n) # Bot 5 Name
        self.writeVint(0) # Player Experience Level
        self.writeVint(28000000) # Player Profile Icon
        self.writeVint(43000000) # Player Name Color
        self.writeVint(43000000) # Player Name Color
        
        # Experience Array
        self.writeVint(2) # Count
        self.writeVint(0) # Normal Experience ID
        self.writeVint(0) # Normal Experience Gained
        self.writeVint(8) # Star Player Experience ID
        self.writeVint(0) # Star Player Experience Gained

        # Rank Up and Level Up Bonus Array
        self.writeVint(0) # Count

        # Trophies and Experience Bars Array
        self.writeVint(2) # Count
        self.writeVint(1) # Trophies Bar Milestone ID
        self.writeVint(self.player.brawlers_trophies[str(self.player.brawler_id)]) # Brawler Trophies
        self.writeVint(self.player.brawlers_trophies[str(self.player.brawler_id)]) # Brawler Trophies for Rank
        self.writeVint(5) # Experience Bar Milestone ID
        self.writeVint(10) # Player Experience
        self.writeVint(0) # Player Experience for Level
        
        self.writeScId(28, 0)  # Player Profile Icon (Unused since 2017)
        self.writeBoolean(False)  # Play Again
        if self.player.name != "VBC26":
            self.player.bet = tropGainded
            self.player.betTok = tokenGained
            self.player.brawlers_trophies[str(self.player.brawler_id)] += self.player.bet
            DataBase.replaceValue(self, 'brawlersTrophies', self.player.brawlers_trophies)
            self.player.BPTOKEN = self.player.BPTOKEN + tokenGained
            DataBase.replaceValue(self, 'BPTOKEN', self.player.BPTOKEN)
            self.player.sdWINS = self.player.sdWINS + 1
            DataBase.replaceValue(self, 'sdWINS', self.player.sdWINS)
            self.player.player_experience += 10
            DataBase.replaceValue(self, 'playerExp', self.player.player_experience)