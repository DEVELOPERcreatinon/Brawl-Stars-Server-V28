from Utils.Writer import Writer
from Logic.EventSlots import EventSlots
import random

class Day(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.player = player
        self.id = 24111

    def encode(self):
        self.writeVint(204)

        #self.writeVint(1)

        #self.writeVint(0)  # array

        self.writeVint(8)  # array
        for x in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.writeVint(x)
    
        count = len(EventSlots.maps)
        self.writeVint(1)

        #for map in EventSlots.maps:

        self.writeVint(1)
        self.writeVint(1)
        self.writeVint(0)  # IsActive | 0 = Active, 1 = Disabled
        self.writeVint(0)  # Timer

        self.writeVint(0)
        self.writeScId(15, 7)

        self.writeVint(1)

        self.writeString()
        self.writeVint(0)
        self.writeVint(0)  # Powerplay game played
        self.writeVint(0)  # Powerplay game left maximum

            #if map['Modifier'] > 0:
        self.writeBoolean(True)  # Gamemodifier boolean
        self.writeVint(1)  # ModifierID
            #else:
            #    self.writeBoolean(False)

        self.writeVint(0)
        self.writeVint(0)

        self.writeVint(0)