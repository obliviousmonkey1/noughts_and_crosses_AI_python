from model import *
from view import *

class Controller:
    def __init__(self, model, ui) -> None:
        self._model = model 
        self._view = ui
        self._view.register(self)
    
    def gameOn(self) -> bool:
        return self._model.ended

    def getTurn(self):
        if (self._model.turn % 2) != 0:
           self._view.getPlayerPos()
        else:
            self.ai()
    
    def player(self, pos):
        result = self._model.playerGo(pos)
        self._view.displayCurrentBoardConfig()
        if result == 1:
            # player won 
            self._view.gameEnded('PLAYER WON')
            self._model.decreaseChance()
        elif result == 0:
            # draw
            self._view.gameEnded('DRAW')

    def ai(self):
        result = self._model.haveGo()
        self._view.displayCurrentBoardConfig()
        if result == 1:
            # ai won 
            self._view.gameEnded('AI WON')
            self._model.increaseChance()
        elif result == 0:
            # draw
            self._view.gameEnded('DRAW')


    
    def getCurrentBoard(self) -> str:
        res = ''
        for i in range(9):
            if self._model.currentNode.config[i] == -1:
                res += '-'
            elif (self._model.currentNode.config[i] % 2) != 0:
                res += 'X'
            else:
                res += 'O'
        return res 

while __name__ == "__main__":
    models = AI()
    ui = UI()
    c = Controller(models, ui)
    ui.mainloop()
    break

