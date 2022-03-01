class UI:
    def __init__(self) -> None:
        self._controller = None
        self._a = 0
        self.gameRunning = True

    def register(self, controller):
        self._controller = controller


    def displayCurrentBoardConfig(self):
        res = self._controller.getCurrentBoard()
        print(res[:3])
        print(res[3:6])     
        print(res[6:])
        print('\n')

    def gameEnded(self, result):
        print(result)

    def getPlayerPos(self):
        pos = int(input('enter pos >'))
        self._controller.player(pos)

    def mainloop(self):
        while self.gameRunning:
            if not self._controller.gameOn():
                self._controller.getTurn()
            else:
                if str(input('Game has ended would you like to play again ? (y/n) >')) == 'n':
                    self.gameRunning = False
                else:
                    self._controller.resetGame()
        