# In Server/Home/LobbyInfoMessage.py
from Utils.Writer import Writer
from datetime import datetime
from ping3 import ping

class LobbyInfoMessage(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.id = 23457
        self.player = player

    def encode(self):
        now = datetime.now()
        domain = '192.168.0.107'
        ping_ms = self.get_ping(domain)

        # Construct the message
        server_info = (
            f'Darty Brawl\n'
            f'TG: @DZDZDZ123rt\n'
            f'Server: none\n'
            f'Ping: {ping_ms}ms\n'
            f'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'  # Creates 15 new lines
        )

        self.writeVint(0)
        self.writeString(server_info)
        self.writeVint(0)

    def get_ping(self, domain):
        ping_seconds = ping(domain)
        if ping_seconds is None:
            return 'N/A'
        
        ping_ms = int(ping_seconds * 800)
        return '<1' if ping_ms == 0 and ping_seconds > 0 else ping_ms