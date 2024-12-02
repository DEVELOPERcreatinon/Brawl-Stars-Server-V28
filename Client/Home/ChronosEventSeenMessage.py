from Utils.Reader import BSMessageReader
from Logic.Commands.Client.LogicOffersChangedCommand import LogicOffersChangedCommand


class ChronosEventSeenMessage(BSMessageReader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        pass

    def process(self):
        LogicOffersChangedCommand(self.client, self.player).send()