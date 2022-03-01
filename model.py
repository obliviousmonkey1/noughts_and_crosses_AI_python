from random import randint, random
import pickle

CHANGE_FACTOR = 0.001
 
class DecisionTree:
    def __init__(self):
        self.p: float = 1
        self.config: list[int] = [-1 for _ in range(9)]
        self.children: list[DecisionTree] = []
 
    def display(self):
        # lots of output!!
        print(f'p: {self.p}, config: {self.config}')
        for child in self.children:
            child.display()
 
def buildTree(dt, options=9, turn=0):
    # find out all indices of -1 in config
    possibilities = []
    for index, val in enumerate(dt.config):
        if val == -1:
            possibilities.append(index)
 
    # for every child, create a new child with
    # a new config
    for poss in possibilities:
        child = DecisionTree()
        # inherit the parent node's configuration
        child.config = dt.config[:]

        # set the new turn on the configuration
        child.config[poss] = turn

        # set the initial probability (normal distrubution)
        child.p = 1/options

        # add the child to the parent's children list
        dt.children.append(child)

        # recursively call this function on the child
        buildTree(child, options-1, turn+1)
    return dt

def checkWon(config):
    # create a new configuration where noughts (even placemennt) are 0,
    # crosses (odd placements) are 1 and blanks are -1
    baseConfig = []
    for n in config:
        if n % 2 == 0:
            baseConfig.append(0)
        elif n % 2 == 1 and n != -1:
            baseConfig.append(1)
        else:
            baseConfig.append(-1)
 
    # check for vertical winning positions
    for offset in range(0, 6+1, 3):
        if baseConfig[0+offset] == baseConfig[1+offset] == baseConfig[2+offset] != -1:
            return True

    # check for horizonal winning positions
    for offset in range(0, 2+1):
        if baseConfig[0+offset] == baseConfig[3+offset] == baseConfig[6+offset] != -1:
            return True
 
    # check for diagonal winning positions
    if baseConfig[0] == baseConfig[4] == baseConfig[8] != -1:
        return True
    if baseConfig[2] == baseConfig[4] == baseConfig[6] != -1:
        return True
   
    return False
 
def checkDraw(config):
    for val in config:
        if val == -1:
            return False
    return True
 
def playGameNaive(dt: DecisionTree):
    currentNode = dt
    turn = 0
    while not (checkDraw(currentNode.config) or checkWon(currentNode.config)):
        randomPosition = randint(0, 8)
        while currentNode.config[randomPosition] != -1:
            randomPosition = randint(0, 8)
        newConfig = currentNode.config[:]
        newConfig[randomPosition] = turn
        for child in currentNode.children:
            if child.config == newConfig:
                currentNode = child
                break
        turn += 1

def playGame(dt: DecisionTree):
    currentNode = dt
    turn = 0
 
    # record the child indices taken
    path = []
    while not (checkDraw(currentNode.config) or checkWon(currentNode.config)):
        # chose a child based on the cumulative probabilities of the children
        randomP = random()
        cumulativeP = 0
        for index, child in enumerate(currentNode.children):
            cumulativeP += child.p
            #assert cumulativeP <= 1.01, f"cumulative frequency >1: {cumulativeP}"
            if randomP <= cumulativeP:
                # set the currentNode and include the index of children to path
                # to track back through the path
                currentNode = child
                path.append(index)
                break
        #print(currentNode.config)
        turn += 1 

    # if noughts have won...
    if checkWon(currentNode.config) and turn % 2 == 1:
        # iterate over path and strengthen all noughts turns
        #print("\nNew Game")
        currentNode = dt
        for i, childIdx in enumerate(path):
            if i % 2 == 0:
                # strengthen the edge to childIdx of children
                valueToAdd = (1 - currentNode.children[childIdx].p) * CHANGE_FACTOR
                #print(f"value to add is {valueToAdd}")
                if valueToAdd > 0:
                    valueToSubtract = valueToAdd / (len(currentNode.children) - 1)
                    currentNode.children[childIdx].p += valueToAdd
                    #print(f"subtracting {valueToSubtract} from {childIdx}")
                    for otherChildIdx in range(len(currentNode.children)):
                        if otherChildIdx != childIdx:
                            currentNode.children[otherChildIdx].p -= valueToSubtract
            currentNode = currentNode.children[childIdx]
        return 1
    # if noughts have lost...
    elif checkWon(currentNode.config) and turn % 2 == 0:
        # iterate over path and weaken all noughts turns
        currentNode = dt
        for i, childIdx in enumerate(path):
            if i % 2 == 0:
                # weaken the edge to childIdx of children
                valueToSubtract = (1 - currentNode.children[childIdx].p) * CHANGE_FACTOR
                if valueToSubtract > 0:
                    currentNode.children[childIdx].p -= valueToSubtract
                    valueToAdd = valueToSubtract / (len(currentNode.children) - 1)

                    for otherChildIdx in range(len(currentNode.children)):
                        if otherChildIdx != childIdx:
                            currentNode.children[otherChildIdx].p += valueToAdd
            currentNode = currentNode.children[childIdx]
        return -1
    # if its a draw
    else:
        # leave path unchanged
        return 0


class AI:
    def __init__(self) -> None:
        self.dt = DecisionTree()
        self.currentNode = self.dt
        self.gameConfig = []
        self.turn = 0
        self.difficulty = 1 # 1 or 0 
        self.ended = False
        self.path = []
        self.developStrategy()

    def developStrategy(self, n: int = 10000):
        buildTree(self.dt)
        for _ in range(n):
            playGame(self.dt)

    def increaseChance(self):
        # iterate over path and strengthen all noughts turns
        currentNode = self.dt
        for i, childIdx in enumerate(self.path):
            if i % 2 == 0:
                # strengthen the edge to childIdx of children
                valueToAdd = (1 - currentNode.children[childIdx].p) * CHANGE_FACTOR
                #print(f"value to add is {valueToAdd}")
                if valueToAdd > 0:
                    valueToSubtract = valueToAdd / (len(currentNode.children) - 1)
                    currentNode.children[childIdx].p += valueToAdd
                    #print(f"subtracting {valueToSubtract} from {childIdx}")
                    for otherChildIdx in range(len(currentNode.children)):
                        if otherChildIdx != childIdx:
                            currentNode.children[otherChildIdx].p -= valueToSubtract
            currentNode = currentNode.children[childIdx]

    def decreaseChance(self):
        # iterate over path and weaken all noughts turns
        currentNode = self.dt
        for i, childIdx in enumerate(self.path):
            if i % 2 == 0:
                # weaken the edge to childIdx of children
                valueToSubtract = (1 - currentNode.children[childIdx].p) * CHANGE_FACTOR
                if valueToSubtract > 0:
                    currentNode.children[childIdx].p -= valueToSubtract
                    valueToAdd = valueToSubtract / (len(currentNode.children) - 1)

                    for otherChildIdx in range(len(currentNode.children)):
                        if otherChildIdx != childIdx:
                            currentNode.children[otherChildIdx].p += valueToAdd
            currentNode = currentNode.children[childIdx]

    def haveGo(self):
        randomP = random()
        cumulativeP = 0
        for index, child in enumerate(self.currentNode.children):
            cumulativeP += child.p
            #assert cumulativeP <= 1.01, f"cumulative frequency >1: {cumulativeP}"
            if randomP <= cumulativeP:
                # set the currentNode and include the index of children to path
                # to track back through the path
                self.currentNode = child
                self.path.append(index)
                break
        #print(currentNode.config)
        self.turn += 1 

        result = -1
        if checkDraw(self.currentNode.config):
            result = 0
            self.ended = True 
        elif checkWon(self.currentNode.config):
            result = 1
            self.ended = True 

        return result 

    def playerGo(self, pos):
        self.currentNode = self.currentNode.children[pos]
        self.path.append(pos)
        self.turn += 1 

        result = -1
        if checkDraw(self.currentNode.config):
            result = 0
            self.ended = True
        elif checkWon(self.currentNode.config):
            result = 1
            self.ended = True 

        return result 
