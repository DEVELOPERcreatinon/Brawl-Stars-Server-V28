from Utils.Writer import Writer


class DevMessage(Writer):

    def __init__(self, client, player):
        super().__init__(client)
        self.id = 28282
        self.player = player

    def encode(self):
        pass
