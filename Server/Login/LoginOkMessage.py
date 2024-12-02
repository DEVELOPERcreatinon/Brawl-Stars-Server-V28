import time

from Utils.Writer import Writer


class LoginOkMessage(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.player = player
        self.id = 20104
        self.version = 1

    def encode(self):
        # Account ID
        self.writeInt(0)
        self.writeInt(self.player.low_id)

        # Home ID
        self.writeInt(0)
        self.writeInt(self.player.low_id)

        self.writeString(self.player.token)
        self.writeString()
        self.writeString()

        self.writeInt(36)
        self.writeInt(218)
        self.writeInt(1)

        self.writeString("prod")

        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)

        self.writeString()
        self.writeString()
        self.writeString()

        self.writeInt(0)

        self.writeString()
        self.writeString("RU")
        self.writeString()

        self.writeInt(1)
        self.writeString()

        self.writeInt(2)
        self.writeString("")
        self.writeString("")
        
        self.writeInt(2)
        self.writeString('')
        self.writeString('')
