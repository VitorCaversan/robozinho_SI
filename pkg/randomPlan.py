from ctypes import sizeof
from random import randint
import re
from shutil import move
from unittest import result
from state import State
from graph import Graph

class RandomPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.searchGraph = Graph()
        self.victimsGraph = Graph()

    
    def setWalls(self, walls):
        row = 0
        col = 0
        for i in walls:
            col = 0
            for j in i:
                if j == 1:
                    self.walls.append((row, col))
                col += 1
            row += 1
       
        
    def updateCurrentState(self, state):
         self.currentState = state

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """


        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return False

        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
        
        ## vai para cima de uma parede
        if (toState.row, toState.col) in self.walls:
            return False

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                return False
        
        return True

    def isPossibleToMovePositionsOnly(self, col, row):
        """ Verifies if it is possible to move to the given column and row """

        ## vai para fora do labirinto
        if (col < 0 or row < 0):
            return False

        if (col >= self.maxColumns or row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
        
        ## vai para cima de uma parede
        if (row, col) in self.walls:
            return False

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = row - self.currentState.row
        delta_col = col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                return False
        
        return True

    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))

    def getCurrentNodeId(self):
        return (self.currentState.row*(self.maxColumns)) + self.currentState.col

    ##################### FINDING VICTIMS SECTION ##############################
    def chooseNextPositionWisely(self):
        possibilities = ["L", "SE", "S", "SO", "O", "NO", "N", "NE"] 
        movePos       = {"L"  : (0, 1),
                         "SE" : (1, 1),
                         "S"  : (1, 0),
                         "SO" : (1, -1),
                         "O"  : (0, -1),
                         "NO" : (-1, -1),
                         "N"  : (-1, 0),
                         "NE" : (-1, 1)}

        iterator     = 0
        movDirection = possibilities[iterator]
        futureLine   = self.currentState.row + movePos[movDirection][0]
        futureCol    = self.currentState.col + movePos[movDirection][1]
        state        = State(futureLine, futureCol)

        while self.searchGraph.__contains__(futureLine, futureCol, self.maxColumns) or not self.isPossibleToMove(state):
            iterator    += 1

            # If there is no place to go, it returns by the path it came (the parent nodes)
            if iterator > 7:
                currentNodeId = self.getCurrentNodeId()
                currentNode = self.searchGraph.getNode(currentNodeId)
                parentNode = self.searchGraph.getNode(currentNode.getParentNodeId())
                state.row = parentNode.line
                state.col = parentNode.column

                parentDirectionY = parentNode.line - currentNode.line
                parentDirectionX = parentNode.column - currentNode.column
                iterator2 = 0
                flag = 0
                while (0 == flag): # Finds the direction of the parent in the possibilities array
                    if (movePos[possibilities[iterator2]][0] == parentDirectionY and movePos[possibilities[iterator2]][1] == parentDirectionX):
                        flag = 1
                        movDirection = possibilities[iterator2]
                        break
                    
                    iterator2 += 1

                break
            else:
                movDirection = possibilities[iterator]
                futureLine   = self.currentState.row + movePos[movDirection][0]
                futureCol    = self.currentState.col + movePos[movDirection][1]
                state.row    = futureLine
                state.col    = futureCol           


        return movDirection, state

    def randomizeNextPosition(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1),
                    "NE" : (-1, 1),
                    "NO" : (-1, -1),
                    "SE" : (1, 1),
                    "SO" : (1, -1)}

        rand = randint(0, 7)
        movDirection = possibilities[rand]
        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

        return movDirection, state


    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        """result = self.randomizeNextPosition()

        while not self.isPossibleToMove(result[1]) or self.searchGraph.__contains__(result[1].row, result[1].col, self.maxColumns):
            result = self.randomizeNextPosition()"""

        result = self.chooseNextPositionWisely()

        diagonal = ["NE", "NO", "SE", "SO"]

        parentNodeId = self.getCurrentNodeId()
        self.searchGraph.addNode(result[1].row, result[1].col, self.maxColumns, parentNodeId)

        if result[0] in diagonal:
            self.searchGraph.addEdge(self.currentState.row, self.currentState.col, result[1].row, result[1].col, self.maxColumns, 1.5)
        else:
            self.searchGraph.addEdge(self.currentState.row, self.currentState.col, result[1].row, result[1].col, self.maxColumns, 1)


        return result

    ##################### RETURNING TO BASE SECTION #############################

    # Tries to find a different direction, given a starting one and following a priority array
    def alternativeDirection(self, startingDirection):
        possibilities         = ["L", "SE", "S", "SO", "O", "NO", "N", "NE"] # Priority array
        possibilitiesRelation = {"L"  : (0, 0),
                                 "SE" : (1, 0),
                                 "S"  : (2, 0),
                                 "SO" : (3, 0),
                                 "O"  : (4, 0),
                                 "NO" : (5, 0),
                                 "N"  : (6, 0),
                                 "NE" : (7, 0)}
        movePos               = {"L"  : (0, 1),
                                 "SE" : (1, 1),
                                 "S"  : (1, 0),
                                 "SO" : (1, -1),
                                 "O"  : (0, -1),
                                 "NO" : (-1, -1),
                                 "N"  : (-1, 0),
                                 "NE" : (-1, 1)}

        iterator     = possibilitiesRelation[startingDirection][0]
        iterator    += 1
        iterator     = iterator % 8
        movDirection = possibilities[iterator]
        futureLine   = self.currentState.row + movePos[movDirection][0]
        futureCol    = self.currentState.col + movePos[movDirection][1]
        state        = State(futureLine, futureCol)

        while not self.isPossibleToMove(state):
            iterator += 1
            iterator =  iterator % 8

            movDirection = possibilities[iterator]
            futureLine   = self.currentState.row + movePos[movDirection][0]
            futureCol    = self.currentState.col + movePos[movDirection][1]
            state.row    = futureLine
            state.col    = futureCol

        return movDirection, state

    def directionToReturn(self, baseCol, baseLine):
        currentNodeId = self.getCurrentNodeId()
        currentNode   = self.searchGraph.getNode(currentNodeId)

        deltaCol  = baseCol - (currentNode.column)
        deltaLine = baseLine - (currentNode.line)

        state        = State(currentNode.line, currentNode.column)
        movDirection = "NO"

        # Basic idea: try to go in the direction of the base. If it happens to be a wall,
        # try to go another way following an array priority.
        if (deltaCol < 0) and (deltaLine < 0):
            if self.isPossibleToMovePositionsOnly((state.col - 1), (state.row - 1)):
                movDirection = "NO"
                state.row    = (currentNode.line   - 1)
                state.col    = (currentNode.column - 1)
            else:
                result = self.alternativeDirection("NO")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol == 0) and (deltaLine < 0):
            if self.isPossibleToMovePositionsOnly((state.col), (state.row - 1)):
                movDirection = "N"
                state.row    = (currentNode.line   - 1)
                state.col    = currentNode.column
            else:
                result = self.alternativeDirection("N")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol > 0) and (deltaLine < 0):
            if self.isPossibleToMovePositionsOnly((state.col + 1), (state.row - 1)):
                movDirection = "NE"
                state.row    = (currentNode.line   - 1)
                state.col    = (currentNode.column + 1)
            else:
                result = self.alternativeDirection("NE")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol > 0) and (deltaLine == 0):
            if self.isPossibleToMovePositionsOnly((state.col + 1), (state.row)):
                movDirection = "L"
                state.row    = currentNode.line
                state.col    = (currentNode.column + 1)
            else:
                result = self.alternativeDirection("L")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol > 0) and (deltaLine > 0):
            if self.isPossibleToMovePositionsOnly((state.col + 1), (state.row + 1)):
                movDirection = "SE"
                state.row    = (currentNode.line   + 1)
                state.col    = (currentNode.column + 1)
            else:
                result = self.alternativeDirection("SE")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol == 0) and (deltaLine > 0):
            if self.isPossibleToMovePositionsOnly((state.col), (state.row + 1)):
                movDirection = "S"
                state.row    = (currentNode.line   + 1)
                state.col    = (currentNode.column)
            else:
                result = self.alternativeDirection("S")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol < 0) and (deltaLine > 0):
            if self.isPossibleToMovePositionsOnly((state.col - 1), (state.row + 1)):
                movDirection = "SO"
                state.row    = (currentNode.line   + 1)
                state.col    = (currentNode.column - 1)
            else:
                result = self.alternativeDirection("SO")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col
        elif (deltaCol < 0) and (deltaLine == 0):
            if self.isPossibleToMovePositionsOnly((state.col + 1), (state.row)):
                movDirection = "O"
                state.row    = (currentNode.line)
                state.col    = (currentNode.column + 1)
            else:
                result = self.alternativeDirection("O")
                movDirection = result[0]
                state.row    = result[1].row
                state.col    = result[1].col

        return movDirection, state

    def returnToBase(self, baseCol, baseLine):

        result = self.directionToReturn(baseCol, baseLine)

        diagonal = ["NE", "NO", "SE", "SO"]

        parentNodeId = self.getCurrentNodeId()
        self.searchGraph.addNode(result[1].row, result[1].col, self.maxColumns, parentNodeId)

        if result[0] in diagonal:
            self.searchGraph.addEdge(self.currentState.row, self.currentState.col, result[1].row, result[1].col, self.maxColumns, 1.5)
        else:
            self.searchGraph.addEdge(self.currentState.row, self.currentState.col, result[1].row, result[1].col, self.maxColumns, 1)


        return result
