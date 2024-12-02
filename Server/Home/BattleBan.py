from Utils.Writer import Writer

class BattleBan(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.id = 22151
        self.client = client
        self.player = player
        
    def encode(self):
        pass