import numpy as np
from random import randint, shuffle
from state import State

class ScrtPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, homeState, model, name = "none", mesh = "square", victims = [], visited = [], tempo = 400):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.model = model

        inv = State(goal.col, goal.row)
        self.goalPos = inv
        self.actions = []
        self.victims = victims
        self.home = homeState
        self.maxTime = tempo
        
        self.map = np.ones((maxRows, maxColumns))
        for state in visited:
            self.map[state.row][state.col] = 0

        nVictims = len(self.victims)

        #print("nVitimas")
        #print(nVictims)
        
        # Calcula uma matriz de distâncias entre as vitimas, para evitar recalcular no futuro
        self.matrizDist = np.zeros((nVictims, nVictims))
        for y in range(0, nVictims):
            for x in range(0, nVictims):
                # (coord, id, grav, classe)
                victimX = self.victims[x][0]
                victimY = self.victims[y][0]
                coord1 = State(victimX[0], victimX[1])
                coord2 = State(victimY[0], victimY[1])
                # State(y, x)
                self.matrizDist[y][x] = self.AEstrela(coord1, coord2)[0][1]

        #print("Matriz de distancias")
        print(self.matrizDist)

        # Calcula um caminho a ser seguido para resgatar as vitimas
        solucao = self.calcularSolucao()
        caminho = solucao

        self.moves = []
        firstVictim = self.victims[caminho[0]][0]
        firstCoord = State(firstVictim[0], firstVictim[1])

        
        # Cria a sequencia de ações que guia o agente do inicio até a primeira vitima
        self.criarPlano(self.goalPos, firstCoord)
        
        # Cria a sequencia de ações que guia o agente entre as vitimas

        for v in range(1, len(caminho)):
            currentVictim = self.victims[caminho[v - 1]][0]
            currentCoord = State(currentVictim[0], currentVictim[1])
            nextVictim = self.victims[caminho[v]][0]
            nextCoord = State(nextVictim[0], nextVictim[1])
            self.criarPlano(currentCoord, nextCoord)

        lastVictim = self.victims[caminho[len(caminho) - 1]][0]
        lastCoord = State(lastVictim[0], lastVictim[1])

        # Cria a sequencia de ações que guia o agente da ultima vitima até o inicio
        self.criarPlano(lastCoord, self.goalPos)

        

    
    # Algoritmo A*
    # Recebe dois States(y,x): start -> target
    # Retorna: current ("nó atual") e closed ("nós explorados")
    # A partir de current.currentCostG temos o custo do caminho start -> target
    # Usando closed podemos descobrir o caminho
    def AEstrela(self, start, target):
        open = []
        closed = []

        def euclidianDistance(p1, p2):
            return ((p1.row - p2.row)**2 + (p1.col - p2.col)**2)**(0.5)

        open.append([start, 0.0, euclidianDistance(start, target), start])

        costs = np.ones((self.maxRows, self.maxColumns)) * 100000.0
        costs[start.row][start.col] = euclidianDistance(start, target) + 0.0

        while len(open) != 0:
            current = min(open, key = lambda t: t[1])
            open.remove(current)
            closed.append(current)

            currentState, currentCostG, currentCostH, currentParent = current

            if currentState == target:
                return current, closed

            currentState = current[0]
            neighbors = []

            neighbors.append(State(currentState.row + 1, currentState.col)) # N
            neighbors.append(State(currentState.row, currentState.col + 1)) # E
            neighbors.append(State(currentState.row - 1, currentState.col)) # S
            neighbors.append(State(currentState.row, currentState.col - 1)) # W

            neighbors.append(State(currentState.row + 1, currentState.col + 1)) # NE
            neighbors.append(State(currentState.row - 1, currentState.col + 1)) # SE
            neighbors.append(State(currentState.row - 1, currentState.col - 1)) # SW
            neighbors.append(State(currentState.row + 1, currentState.col - 1)) # NW

            for neighbor in neighbors:
                closedStates, closedCostsG, closedCostsH, closedParents = list(map(list, zip(*closed)))

                def isTransversable(p1, p2, map):
                    # Horizontal, vertical
                    cost = 1.0

                    if (p2.col < 0 or p2.row < 0):
                        return False, cost

                    if (p2.col >= self.maxColumns or p2.row >= self.maxRows):
                        return False, cost
                
                    if map[p2.row][p2.col] == 1:
                        return False, cost

                    # Diagonal
                    delta_row = p2.row - p1.row
                    delta_col = p2.col - p1.col
                    ## o movimento eh na diagonal
                    if (delta_row != 0 and delta_col != 0):
                        cost = 1.5
                        
                        # Pode dar problema
                        # if map[p1.row + delta_row][p1.col] == 1 and map[p1.row][p1.col + delta_col] == 1:
                        #     return False, cost

                    return True, cost

                transversable, cost = isTransversable(currentState, neighbor, self.map)
                if not transversable or neighbor in closedStates:
                    continue

                openStates = []
                openCosts = []
                openParents = []

                try:
                    openStates, openCostsG, openCostsH, openParents = list(map(list, zip(*open)))
                except:
                    pass

                if neighbor not in openStates or costs[neighbor.row][neighbor.col] > currentCostG + cost:
                    costs[neighbor.row][neighbor.col] = currentCostG + cost
                    if neighbor not in openStates:
                        open.append([neighbor, currentCostG + cost, euclidianDistance(neighbor, target), currentState])
                    else:
                        index = openStates.index(neighbor)
                        open[index][1] = currentCostG + cost
                        open[index][2] = euclidianDistance(neighbor, target)
                        open[index][3] = currentState

        return [(-1, -1, -1, -1), (-1, -1, -1, -1)]
        # Isso nunca deve acontecer
        # Significa que não existe caminho entre a posição atual e o objetivo
        # Mapa mal feito
    
    # Função responsável por calcular a ordem de visita das vitimas
    # Retorna um caminho a ser seguido
    # O caminho é um array de indices, representa a ordem de visita das vitimas.
    # caminho = [0, 3, 6, 2, 1, 5, 4] por exemplo
    # Qualquer melhoria do algoritmo dever ser aqui!
    def calcularSolucao(self):
        pop = []

        # Etapa: Inicialização
        for i in range(0, 200): # 200 individuos na populacao
            cromossomo = np.zeros(len(self.victims))
            score = 0.0
            caminho = []
            custo_caminho = 0.0
            for j in range(0, len(self.victims)):
                cromossomo[j] = 1 # Array de 0's ou 1's que determinam se tal vitima vai ser socorrida ou nao

                if cromossomo[j] == 1: # Adiciona a vitima j no caminho e soma o valor dela no score da solucao
                    caminho.append(j)
                    score += self.victims[j][3]
                
            shuffle(caminho) # Embaralha o caminho ordenado, exemplo: [0, 1, 2, 3, 4] => [1, 3, 0, 2, 4]

            # 2-opt search, algoritmo de busca local no espaço de estados do problema do caixeiro viajante.
            # Essencialmente tenta melhorar uma solução já calculada, desembaralhando caminhos entrelaçados e ineficientes.
            # Uso 2-opt na solução criada aleatoriamente pelo shuffle

            def cost_change(cost_mat, n1, n2, n3, n4):
                return cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]

            def two_opt(route, cost_mat):
                best = route
                improved = True
                while improved:
                    improved = False
                    for i in range(1, len(route) - 2):
                        for j in range(i + 1, len(route)):
                            if j - i == 1: continue
                            if cost_change(cost_mat, best[i - 1], best[i], best[j - 1], best[j]) < 0:
                                best[i:j] = best[j - 1:i - 1:-1]
                                improved = True
                    route = best
                return best

            two_opt(caminho, self.matrizDist)

            goalState = self.goalPos
            indexFirstVictim = caminho[0]
            indexLastVictim = caminho[len(caminho) - 1]
            victimX = self.victims[indexFirstVictim][0]
            victimY = self.victims[indexLastVictim][0]
            coord1 = State(victimX[0], victimX[1])
            coord2 = State(victimY[0], victimY[1])

            # Calculo do custo do caminho
            custo_caminho += self.AEstrela(goalState, coord1)[0][1] # Caminho até a primeira vitima
            for j in range(1, len(caminho)): # Caminho entre as vitimas
                custo_caminho += self.matrizDist[caminho[j - 1]][caminho[j]]
            custo_caminho += self.AEstrela(coord2, goalState)[0][1] # Caminho até a ultima vitima

            # Cromossomo não é utilizado, por enquanto
            pop.append([cromossomo, caminho, score, custo_caminho])

        best = ([], [], 0.0, 0.0)

        for ind in pop: # Escolhe o melhor individuo da populacao
            score = ind[2]
            custo = ind[3]

            if score > best[2] and custo < self.maxTime: # E se não tiver nenhum individuo? Resolver esse problema
                best = ind

        return best[1] # Melhor caminho encontrado na população

    def updateCurrentState(self, state):
        self.currentState = state

    def chooseAction(self):
        """ 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro
        if len(self.moves) != 0: 
            result = self.moves.pop() # Direcao e state esperado
        else: 
            result = ("nop", State(-1, -1))

        return result
    
    # Cria uma lista de ações com base em um start e um target (start -> target)
    # As ações guiam o agente até o target
    # Essencialmente transforma o caminho calculado no A* em algo para ser executado pelo agente
    def criarPlano(self, atual, next):
        
        #atual = self.goalPos
        #victim = self.victims[21][0]
        #victimCoord = State(victim[0], victim[1])
        victimCoord = next
        #print(atual, victimCoord)
        current, closed = self.AEstrela(atual, victimCoord)

        currentState, currentCostG, currentCostH, currentParent = current
        closedStates, closedCostsG, closedCostsH, closedParents = list(map(list, zip(*closed)))

        def getOrientation(parent, current):
            possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
            movePos = [ (-1, 0),
                    (1, 0),
                    (0, 1),
                    (0, -1),
                    (-1, 1),
                    (-1, -1),
                    (1, 1),
                    (1, -1)]

            yp = parent.row
            xp = parent.col
            yc = current.row
            xc = current.col

            for index in range(0, len(movePos)):
                y = movePos[index][0]
                x = movePos[index][1]
                if yp + y == yc and xp + x == xc:
                    return possibilities[index]

        moves = []
        temp = State(currentState.row, currentState.col)
        moves.append((getOrientation(currentParent, currentState), temp)) # Primeiro passo

        while currentParent != currentState:
            index = closedStates.index(currentParent)
            currentState, currentCostG, currentCostH, currentParent = closed[index]
            temp = State(currentState.row, currentState.col)
            moves.append((getOrientation(currentParent, currentState), temp))

        movesAux = []
        for move in moves:
            movesAux.append(move)
        movesAux.pop()

        movesAux.extend(self.moves)
        self.moves = movesAux