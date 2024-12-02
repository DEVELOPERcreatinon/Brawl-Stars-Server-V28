from Utils.Writer import Writer
class AddFriendFailedMessage(Writer):
    def __init__(self, client, player):
        super().__init__(client)
        self.id = 20112
        self.player = player
    def encode(self):
        self.writeInt(3) # 1 - Добавить не удалось, 2 - У тебя слишком много запросов, 3 - Я хз, 4 - У этого игрока много запросов, 5 - Такого игрока нету