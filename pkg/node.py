class Node:
    def __init__(self, line, col, maxColumns, parentNodeId = 0):
        self.id = (line*(maxColumns)) + col
        self.line = line
        self.column = col
        self.connectedTo = {}
        self.parent = parentNodeId
        self.type = False # o que tem neste quadrado ? false não tem vitima true tem vitima

    def addNeighbor(self, nbrNode, weight = 0): # Weight 0 as default
        self.connectedTo[nbrNode] = weight; 

    def __str__(self):
        return f"{str(self.id)} connected to: {str([nbrNode.id for nbrNode in self.connectedTo])}"

    def getConnection(self):
        # Returns all neighbors keys from a node
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbrNode):
        return self.connectedTo.get(nbrNode)
    
    def getState(self):
        return self.type

    def getParentNodeId(self):
        return self.parent

    def setType(self, type):
        self.type = type