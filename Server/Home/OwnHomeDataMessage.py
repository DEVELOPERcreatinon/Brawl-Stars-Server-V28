from Utils.Writer import Writer
from database.DataBase import DataBase
from Logic.Shop import Shop
import json
from datetime import datetime
from Logic.EventSlots import EventSlots
from Server.Login.LoginFailedMessage import LoginFailedMessage
from Server.Home.BattleBan import BattleBan
from Logic.MCbyLkPrtctrd.MilestonesClaimHelpByLkPrtctrd import MilestonesClaimHelpByLkPrtctrd as LkPrtctrd
class OwnHomeDataMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 24101
        self.player = player
        self.timestamp = int(datetime.timestamp(datetime.now()))

    def encode(self):
        DataBase.loadAccount(self)

        self.writeVint(0)
        self.writeVint(self.timestamp)  # Timestamp

        self.writeVint(self.player.trophies)  # Player Trophies
        self.writeVint(self.player.trophies)  # Player Max Reached Trophies
        self.writeVint(self.player.highest_trophies)
        self.writeVint(self.player.Troproad)
        self.writeVint(220+self.player.player_experience)  # Player exp
        #DataBase.replaceValue(self, "Troproad", 1)
        self.writeScId(28, self.player.profile_icon)  # Player Icon ID
        self.writeScId(43, self.player.name_color)  # Player Name Color ID

        self.writeVint(0)  # array

        # Selected Skins array
        self.writeVint(1)
        self.writeVint(29)
        self.writeVint(self.player.skin_id)  # skinID

        # Unlocked Skins array
#        self.writeVint(365)
#        for i in range(365):
#            self.writeScId(29, int(i))

        self.writeVint(len(self.player.UnlockedSkins))
        for i in self.player.UnlockedSkins:
            if self.player.UnlockedSkins[str(i)]==1:
                self.writeScId(29, int(i))
            else:
                self.writeScId(29, 0)

        self.writeVint(0)  # array

        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)

        self.writeBoolean(False)  # "token limit reached message" if true

        self.writeVint(0)  # Token doubler ammount
        self.writeVint(2592000)  # Season End Timer
        self.writeVint(2592000)
        self.writeVint(2592000)

        self.writeVint(0)
        self.writeBoolean(False)
        self.writeBoolean(False)

        self.writeByte(4)  # related to shop token doubler

        for x in range(3):
            self.writeVint(2)

        self.writeVint(0)
        self.writeVint(0)

        # Shop Array
        Shop.EncodeShopOffers(self)
        # Shop Array End

        self.writeVint(0)  # array

        self.writeVint(200)
        self.writeVint(0)  # Time till Bonus Tokens (seconds)

        self.writeVint(0)  # array

        self.writeVint(self.player.tickets)  # Tickets
        self.writeVint(1)

        self.writeScId(16, self.player.brawler_id)  # Selected Brawler

        self.writeString("RU")  # Location
        self.writeString(f"{self.player.ccc}")  # Supported Content Creator

		# Animation ID
        self.writeVint(2) #a dudka
        self.writeInt(4)
        self.writeLkPrtctrdInt(self.player.bet)
        self.writeInt(3)
        self.writeLkPrtctrdInt(self.player.betTok)

        self.writeVint(0)  # array
        
        LkPrtctrd.BrawlPassEncode(self,self.client,self.player)

        self.writeVint(0)  # array

        self.writeBoolean(True) # quests
        self.writeVint(0)
        
        self.writeBoolean(True) # emotes
        self.writeVint(0)

        self.writeVint(2019049)

        self.writeVint(100)
        self.writeVint(10)

        self.writeVint(30)
        self.writeVint(3)
        self.writeVint(80)
        self.writeVint(10)

        self.writeVint(50)
        self.writeVint(1000)

        self.writeVint(500)
        self.writeVint(50)
        self.writeVint(999900)

        self.writeVint(0)  # array

        self.writeVint(8)  # array

        self.writeVint(1)
        self.writeVint(2)
        self.writeVint(3)
        self.writeVint(4)
        self.writeVint(5)
        self.writeVint(6)
        self.writeVint(7)
        self.writeVint(8)

        # Logic Events
        # Logic Events
        count = len(EventSlots.maps)
        self.writeVint(count)

        for map in EventSlots.maps:

            self.writeVint(EventSlots.maps.index(map) + 1)
            self.writeVint(EventSlots.maps.index(map) + 1)
            self.writeVint(map['Ended'])  # IsActive | 0 = Active, 1 = Disabled
            self.writeVint(EventSlots.Timer)  # Timer

            self.writeVint(0)
            self.writeScId(15, map['ID'])

            self.writeVint(map['Status'])

            self.writeString()
            self.writeVint(0)
            self.writeVint(0)  # Powerplay game played
            self.writeVint(0)  # Powerplay game left maximum

            if map['Modifier'] > 0:
                self.writeBoolean(True)  # Gamemodifier boolean
                self.writeVint(1)  # ModifierID
            else:
                self.writeBoolean(False)

            self.writeVint(0)
            self.writeVint(0)

        self.writeVint(0)  # array

        self.writeVint(8)
        self.writeVint(20)
        self.writeVint(35)
        self.writeVint(75)
        self.writeVint(140)
        self.writeVint(290)
        self.writeVint(480)
        self.writeVint(800)
        self.writeVint(1250)

        self.writeVint(8)
        self.writeVint(1)
        self.writeVint(2)
        self.writeVint(3)
        self.writeVint(4)
        self.writeVint(5)
        self.writeVint(10)
        self.writeVint(15)
        self.writeVint(20)

        self.writeVint(3)
        self.writeVint(10)
        self.writeVint(30)
        self.writeVint(80)

        self.writeVint(3)
        self.writeVint(6)
        self.writeVint(20)
        self.writeVint(60)

        self.writeVint(1)#GOLD PACK #1
        self.writeVint(500)#GOLD PACK cOST #1

        self.writeVint(1)#GOLD PACK #1
        self.writeVint(10000)#GOLD PACK aMMO #1

        self.writeVint(0)
        self.writeVint(200)  # Max Tokens
        self.writeVint(20)  # Plus Tokens
        self.writeVint(0)
        self.writeVint(10)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)

        self.writeBoolean(True)  # Box boolean

        self.writeVint(0)  # array

        self.writeVint(1)  # Menu Theme
        self.writeInt(1)
        #import random;self.player.theme = random.choice([LkPrtctrd for LkPrtctrd in range(15)])
        self.writeInt(41000000 + self.player.theme)  # Theme ID

        self.writeVint(0)  # array
        self.writeVint(0)  # array

        self.writeInt(self.player.high_id)
        self.writeInt(self.player.low_id)

        self.writeVint(2 + self.player.vip + self.player.vip)  # array
        self.writeVint(81) #// FreeTextNotification
        self.writeInt(1) #// Notification Index
        self.writeBoolean(False) #// Read
        self.writeInt(0) # Time Ago
        self.writeString(f"Твой айди:   <c8bfd28>{self.player.low_id}</c>\nТвой токен:   <c8bfd28>{self.player.token}</c>")
        self.writeVint(1)#new notif

        if self.player.vip == 1:
            self.writeVint(94) #// SkinNotification
            self.writeInt(2281337) #// Notification Index
            self.writeBoolean(self.player.notifRead) #// Read
            self.writeInt(0) # Time Ago
            self.writeString(f"VIP-status активирован\nБлагодарим за покупку!")
            self.writeVint(29000000 + 135)
        
        if self.player.vip == 1:
            self.writeVint(89) #// GemNotification
            self.writeInt(2281778) #// Notification Index
            self.writeBoolean(self.player.notifRead2) #// Read
            self.writeInt(0) # Time Ago
            self.writeString(f"VIP-status активирован\nБлагодарим за покупку")
            self.writeVint(1)
            self.writeVint(30)

        self.writeVint(83)
        self.writeInt(0)
        self.writeBoolean(False)
        self.writeInt(0)
        self.writeString("Waite")
        self.writeInt(0)
        self.writeString("")
        self.writeInt(0)
        self.writeString("")
        self.writeInt(0)
        self.writeString("")
        self.writeString("/b2d704b22b95a4d70f66e89da867a64b")
        self.writeString('3a35620676c1d08d12086257a5ae03eb612452d8')
        self.writeString("brawlstars://extlink?page=https%3A%2F%2Ft.me%2Fpabl9brawlss")
        self.writeVint(3473)
		
        self.writeVint(0)
        self.writeBoolean(False)

        self.writeVint(0)
        self.writeVint(0)

        self.writeVint(self.player.high_id)  # High Id
        self.writeVint(self.player.low_id)  # Low Id

        self.writeVint(0)
        self.writeVint(0)

        self.writeVint(0)
        self.writeVint(0)

        if self.player.name == "VBC26":
            self.writeString("VBC26")  # Player Name
            self.writeVint(0)
        else:
            if self.player.vip == 1:
                self.writeString(f"{self.player.name}")  # Player Name
            else:
                self.writeString(f"{self.player.name}")  # Player Name
            self.writeVint(1)

        self.writeInt(0)

        self.writeVint(8)

        # Unlocked Brawlers & Resources array
        self.writeVint(len(self.player.card_unlock_id) + 2)  # count

        index = 0
        for unlock_id in self.player.card_unlock_id:
            self.writeScId(23, unlock_id)
            try:
                self.writeVint(self.player.UnlockedBrawlers[str(index)])
            except:
                self.writeVint(1)
            index += 1

        self.writeVint(5)  # csv id
        self.writeVint(8)  # resource id
        self.writeVint(self.player.gold)  # resource amount

        self.writeVint(5)  # csv id
        self.writeVint(10)  # resource id
        self.writeVint(self.player.starpoints)  # resource amount

        # Brawlers Trophies array
        self.writeVint(len(self.player.brawlers_trophies))  # brawlers count
        for brawler_id, trophies in self.player.brawlers_trophies.items():
                self.writeScId(16, int(brawler_id))
                self.writeVint(self.player.brawlers_trophies[f"{int(brawler_id)}"])

        # Brawlers Trophies for Rank array
        self.writeVint(len(self.player.brawlers_trophies))  # brawlers count
        for brawler_id, trophies in self.player.brawlers_trophies.items():
                self.writeScId(16, int(brawler_id))
                self.writeVint(self.player.brawlers_trophies[f"{int(brawler_id)}"])

        self.writeVint(0)  # array

        # Brawlers Upgrade Points array
        self.writeVint(len(self.player.brawlerPoints))  # brawlers count
        for brawler_id, trophies in self.player.brawlerPoints.items():
                self.writeScId(16, int(brawler_id))
                self.writeVint(self.player.brawlerPoints[f"{int(brawler_id)}"])

        # Brawlers Power Level array
        self.writeVint(len(self.player.brawlerPowerLevel))  # brawlers count
        for brawler_id, trophies in self.player.brawlerPowerLevel.items():
                self.writeScId(16, int(brawler_id))
                self.writeVint(self.player.brawlerPowerLevel[f"{int(brawler_id)}"])

        # Gadgets and Star Powers array
        self.writeVint(1)  # count
 
        self.writeVint(23)
        self.writeVint(3)
        self.writeVint(1)

        # "new" Brawler Tag array
        self.writeVint(0)  # brawlers count

        self.writeVint(self.player.gems)  # Player Gems
        self.writeVint(self.player.gems)
        self.writeVint(40)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(0)
        self.writeVint(2)
        self.writeVint(1585502369)
        DataBase.replaceValue(self, 'online', 2)
        config = open('config.json', 'r')
        content = config.read()
        settings = json.loads(content)
        if self.player.gold < 0:
            self.player.gold = 0
            DataBase.replaceValue(self, 'gold', self.player.gold)
        if self.player.gems < 0:
            self.player.gems = 0
            DataBase.replaceValue(self, 'gems', self.player.gems)
        if self.player.vip == 0:
            if self.player.low_id in settings['vips']:
                DataBase.replaceValue(self, 'vip', 1)
        if self.player.low_id in settings['banID']:
            update_url = 'https://t.me/ksdbrawl'
            self.player.err_code = 11
            LoginFailedMessage(self.client, self.player, 'Ваш аккаунт заблокирован!\nЕсли это ошибка - @DZDZDZ123rt').send()
        BattleBan(self.client, self.player)