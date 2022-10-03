import sys
import os
import time

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentRnd import AgentRnd


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def main():
    # Lê arquivo config.txt
    arq = open(os.path.join("config_data","ambiente.txt"),"r")
    
    arq_texto = []
    for line in arq:
        arq_texto.append(line.split(" ")[1:])

    configDict = {}

    configDict["Te"] = int(arq_texto[0][0])
    configDict["Ts"] = int(arq_texto[1][0])
    configDict["maxCol"] = int(arq_texto[3][0])
    configDict["maxLin"] = int(arq_texto[4][0])

    base = (int(arq_texto[2][0].split(",")[0]), int(arq_texto[2][0].split(",")[1]))

    print("dicionario config: ", configDict)

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configDict["maxLin"], configDict["maxCol"], mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent = base
    model.maze.board.posGoal = base
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria um agente
    agent = AgentRnd(model,configDict)

    ## Ciclo de raciocínio do agente
    agent.deliberate()
    while agent.deliberate() != -1:
        model.draw()
        time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    

if __name__ == '__main__':
    main()
