from sre_parse import State
import sys
import os
import time

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from pkg.model import Model
from pkg.agentRnd import AgentRnd
from pkg.agentScrt import AgentScrt
from pkg.state import State


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def setVictimsList(maze, agent):
    vict = maze.victims #matriz
    victimsList = []
    for row in range(len(vict)):
        for col in range(len(vict[row])):
            id = vict[row][col]
            if id != 0 and id != 42: #tem vitima
                (coll, roww) = (col, row)
                coord = (coll, roww)
                vitalInfo = agent.victimVitalSignalsSensor(id)
                vitalInfo2 = vitalInfo[0]
                grav = vitalInfo2[len(vitalInfo2) - 2]
                classe = vitalInfo2[len(vitalInfo2) - 1]
                victim = (coord, id, grav, classe)
                victimsList.append(victim)
    return victimsList

def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data","teste_ambiente.txt"),"r")
    
    arq_texto = []
    for line in arq:
        arq_texto.append(line.split(" ")[1:])

    configDict = {}

    configDict["Te"] = int(arq_texto[0][0])
    configDict["Ts"] = int(arq_texto[1][0])
    configDict["maxCol"] = int(arq_texto[3][0])
    configDict["maxLin"] = int(arq_texto[4][0])
    Vt = len(arq_texto[5])

    base = (int(arq_texto[2][0].split(",")[0]), int(arq_texto[2][0].split(",")[1]))

    print("dicionario config: ", configDict)

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "teste_ambiente"

    model = Model(configDict["maxLin"], configDict["maxCol"], mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent = base
    model.maze.board.posGoal = base
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    # model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    # model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])
    model.setAgentPos(base[0], base[1])
    model.setGoalPos(base[0], base[1])
    model.draw()

    # Cria um agente
    agent = AgentRnd(model,configDict)

    ## Ciclo de raciocínio do agente
    agent.deliberate()
    while agent.deliberate() != -1:
        model.draw()
        time.sleep(0.1) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()

    searchGraph  = agent.plan.searchGraph
    victimsGraph = agent.plan.victimsGraph
    victims      = agent.victims

    visited = []

    for nodeId in searchGraph.nodeList:
        node = searchGraph.getNode(nodeId)
        state = State(node.line, node.column)
        if state not in visited:
            visited.append(state)

    # for victim in victims:
    #     state = State(victim[0][1], victim[0][0])
    #     if state not in visited:
    #         visited.append(state)

    print(visited)

    print(victims)

    rescuer = AgentScrt(model, configDict, base, victims, visited)

    rescuer.deliberate()
    while rescuer.deliberate() != -1:
        model.draw()
        time.sleep(0.1)
    model.draw

    ####### CALCULANDO METRICAS EXPLORADOR ########
    ve = victimsGraph.numNodes
    pve = ve/Vt

    Te = configDict["Te"]
    te = Te - agent.tl
    tve = te/ve

    victimsListForCalculus = setVictimsList(model.maze, agent)
    victimsGrav = [0, 0, 0, 0]
    for v in victimsListForCalculus:
        if v[3] <= 25:
            victimsGrav[0] += 1
        elif v[3] <= 50:
            victimsGrav[1] += 1
        elif v[3] <= 75:
            victimsGrav[2] += 1
        else:
            victimsGrav[3] += 1

    foundVictimsGrav = [0, 0, 0, 0]
    for v in victims:
        if v[3] <= 25:
            foundVictimsGrav[0] += 1
        elif v[3] <= 50:
            foundVictimsGrav[1] += 1
        elif v[3] <= 75:
            foundVictimsGrav[2] += 1
        else:
            foundVictimsGrav[3] += 1
    veg = (4*foundVictimsGrav[0] + 3*foundVictimsGrav[1] + 2*foundVictimsGrav[2] + foundVictimsGrav[3])
    veg = veg/(4*victimsGrav[0] + 3*victimsGrav[1] + 2*victimsGrav[2] + victimsGrav[3])

    #### CALCULANDO PARA O SOCORRISTA #######
    vs = ve
    pve = vs/Vt

    ts = Te - rescuer.ts
    tvs = ts/vs

    victimsListForCalculus = setVictimsList(model.maze, agent)

    savedVictimsGrav = [0, 0, 0, 0]
    for v in victims:
        if v[3] <= 25:
            savedVictimsGrav[0] += 1
        elif v[3] <= 50:
            savedVictimsGrav[1] += 1
        elif v[3] <= 75:
            savedVictimsGrav[2] += 1
        else:
            savedVictimsGrav[3] += 1
    veg = (4*savedVictimsGrav[0] + 3*savedVictimsGrav[1] + 2*savedVictimsGrav[2] + savedVictimsGrav[3])
    veg = veg/(4*victimsGrav[0] + 3*victimsGrav[1] + 2*victimsGrav[2] + victimsGrav[3])

    print("deu boa")

if __name__ == '__main__':
    main()