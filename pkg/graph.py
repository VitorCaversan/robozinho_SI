from node import Node

class Graph:
    def __init__(self):
        self.nodeList = {}
        self.numNodes = 0
    
    def addNode(self, line, col, maxColumns, parentNodeId = 0, nextMovDirection = "L") -> Node:
        if self.__contains__(line, col, maxColumns):
            newNode = self.getNode((line*(maxColumns)) + col)
        else:
            self.numNodes += 1
            newNode = Node( line, col, maxColumns, parentNodeId, nextMovDirection)
            self.nodeList[newNode.id] = newNode # Adds the new node to the node list
        
        return newNode
      
    def getNode(self, id) -> Node:
        # If node with given id is in Graph then return the node
        
        # use the get method to return the node if it exists
        # otherwise it will return None
        return self.nodeList.get(id)
      
    def __contains__(self, line, col, maxColumns):
        # Check whether node with key is in the Graph
        # returns True or False depending if it's in the list
        key = (line*(maxColumns)) + col
        return key in self.nodeList

    def addEdge(self, fromLine, fromCol, toLine, toCol, maxColumns, weight = 0):
        """
        Add an edge to connect two vertices of t and f with weight
        assuming directed graph
        """
        f = (fromLine*(maxColumns)) + fromCol
        t = (toLine*(maxColumns)) + toCol
        #add vertices if they do not exist
        if f not in self.nodeList:
            nv = self.addNode(fromLine, fromCol, maxColumns)
        if t not in self.nodeList:
            nv = self.addNode(toLine, toCol, maxColumns)
            
        #then add Neighbor from f to t with weight
        self.nodeList[f].addNeighbor(self.nodeList[t], weight)
        print("Node ", f, " added.")
        print(self.nodeList[f].__str__(), "With weight: ", weight)
        
    def getNodes(self):
        # Returns all node keys in the list
        return self.nodeList.keys()

    def getNumberOfNodes(self):
        return self.numNodes

    # Changes the next movement direction of a node in order for the search system not to enter a loop
    def changeNextMovDirectionFromNode(self, nodeId, maxColumns):
        possibilities         = ["L", "S", "O", "N", "NE", "SE", "SO", "NO"] # Priority array
        possibilitiesRelation = {"L"  : (0, 0),
                                 "S"  : (1, 0),
                                 "O"  : (2, 0),
                                 "N"  : (3, 0),
                                 "NE" : (4, 0),
                                 "SE" : (5, 0),
                                 "SO" : (6, 0),
                                 "NO" : (7, 0)}
        movePos               = {"L"  : (0, 1),
                                "SE" : (1, 1),
                                "S"  : (1, 0),
                                "SO" : (1, -1),
                                "O"  : (0, -1),
                                "NO" : (-1, -1),
                                "N"  : (-1, 0),
                                "NE" : (-1, 1)}

        node = self.getNode(nodeId)
        newMovIndex = possibilitiesRelation[node.getnextMovDirection()][0]
        futureLine   = node.line   + movePos[node.getnextMovDirection()][0]
        futureCol    = node.column + movePos[node.getnextMovDirection()][1]

        iterator = 0
        while (self.__contains__(futureLine, futureCol, maxColumns)):
            iterator    += 1
            newMovIndex = (newMovIndex + 1) % 8
            node.nextMovDirection = possibilities[newMovIndex]
            futureLine   = node.line   + movePos[node.getnextMovDirection()][0]
            futureCol    = node.column + movePos[node.getnextMovDirection()][1]
            
            if iterator > 7:
                break