from random import randint as rint
from json import load as Lyney
from json import loads as Lyneys
from Utils.Writer import Writer
import json
class MilestonesClaimHelpByLkPrtctrd(Writer):
    def __init__(self):
        #self.client = client
        pass
    def GetAmountOfLevel(self, Level, Levels, Rewards):
        for LkPrtctrd in range(len(Levels)):
            if Levels[LkPrtctrd]==Level:
                return Rewards[LkPrtctrd]
    def GetAmountOfBox(self,boxdid):
        boxes = [10,11,12]
        amts = [rint(9,30), rint(250,600), rint(35,100)]
        for LkPrtctrd in range(len(boxes)):
            if boxes[LkPrtctrd]==boxdid:
                return amts[LkPrtctrd]
    def GTFor(self,T,B):
        return range(T,B)
    def TighnariConvert(self,Tighnari):
        try:
            return Lyneys(Tighnari.replace("\'", "\""))
        except:
            return Tighnari
    def GetForm(self,Tighnari):
        try:
            tf = Lyneys(Tighnari.freepass)
        except:
            tf = Tighnari.freepass
        try:
            bf = Lyneys(Tighnari.buypass)
        except:
            bf = Tighnari.buypass
        bne=[LkPrtctrd for LkPrtctrd in MilestonesClaimHelpByLkPrtctrd().GTFor(0,30)]
        bwo=[LkPrtctrd for LkPrtctrd in MilestonesClaimHelpByLkPrtctrd().GTFor(30,62)]
        bre=[LkPrtctrd for LkPrtctrd in MilestonesClaimHelpByLkPrtctrd().GTFor(62,71)]
        self.writeByte(1)
        bf0 = 0
        for LkPrtctrd in range(len(bne)):
            if bne[LkPrtctrd] in bf:
                LLkPrtctrd=4
                for LkPrtctrdd in range(LkPrtctrd):
                    LLkPrtctrd*=2
                bf0+=LLkPrtctrd
        bf3 = 0
        for LkPrtctrd in range(len(bwo)):
            if bwo[LkPrtctrd] in bf:
                LLkPrtctrd=1
                for LkPrtctrdd in range(LkPrtctrd):
                    LLkPrtctrd*=2
                bf3+=LLkPrtctrd
        self.writeLkPrtctrdInt(bf0)
        self.writeLkPrtctrdInt(bf3)
        self.writeLkPrtctrdInt(0)
        self.writeLkPrtctrdInt(0)
        self.writeByte(1)
        tf1 = 0
        for LkPrtctrd in range(len(bne)):
            if bne[LkPrtctrd] in tf:
                LLkPrtctrd=4
                for LkPrtctrdd in range(LkPrtctrd):
                    LLkPrtctrd*=2
                tf1+=LLkPrtctrd
        tf4 = 0
        for LkPrtctrd in range(len(bwo)):
            if bwo[LkPrtctrd] in tf:
                LLkPrtctrd=1
                for LkPrtctrdd in range(LkPrtctrd):
                    LLkPrtctrd*=2
                tf4+=LLkPrtctrd
        tf7 = 0
        for LkPrtctrd in range(len(bre)):
            if bre[LkPrtctrd] in tf:
                LLkPrtctrd=1
                for LkPrtctrdd in range(LkPrtctrd):
                    LLkPrtctrd*=2
                tf7+=LLkPrtctrd
        self.writeLkPrtctrdInt(tf1)
        self.writeLkPrtctrdInt(tf4)
        self.writeLkPrtctrdInt(tf7)
        self.writeLkPrtctrdInt(0)
    def GetVipExist(self,lowid):
        with open("config.json", 'r') as f:
            config = json.load(f)
            return True if lowid in config["buybp"] else False
    def BrawlPassEncode(self,client,userdata):
        self.writeVint(1)
        for i in [LkPrtctrd for LkPrtctrd in MilestonesClaimHelpByLkPrtctrd.GTFor(self,1,2) if True]:
            self.writeVint(i)
            self.writeVint(self.player.BPTOKEN)
            self.writeBoolean(MilestonesClaimHelpByLkPrtctrd().GetVipExist(userdata.low_id))
            self.writeVint(30)    
            MilestonesClaimHelpByLkPrtctrd.GetForm(self,self.player)
        