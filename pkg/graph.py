from node import Node

class Graph:
    def __init__(self):
        self.nodeList = {}
        self.numNodes = 0
    
    def addNode(self, line, col, maxColumns):
        self.numNodes += 1
        newNode = Node(line, col, maxColumns)
        self.nodeList[newNode.id] = newNode # Adds the new node to the node list
        
        return newNode
      
    def getNode(self, id):
        # If node with given id is in Graph then return the node
        
        #use the get method to return the node if it exists
        #otherwise it will return None
        return self.nodeList.get(id)
      
    def __contains__(self, line, col, maxColumns):
        # Check whether node with key is in the Graph
        # returns True or False depending if in list
        key = (line*(maxColumns)) + col
        return key in self.nodeList

    def addEdge(self, fLine, fCol, tLine, tCol, maxColumns, weight = 0):
        """
        Add an edge to connect two vertices of t and f with weight
        assuming directed graph
        """
        f = (fLine*(maxColumns)) + fCol
        t = (tLine*(maxColumns)) + tCol
        #add vertices if they do not exist
        if f not in self.nodeList:
            nv = self.addNode(fLine, fCol, maxColumns)
        if t not in self.nodeList:
            nv = self.addNode(tLine, tCol, maxColumns)
            
        #then add Neighbor from f to t with weight
        self.nodeList[f].addNeighbor(self.nodeList[t], weight)
        print("Node ", f, " added.")
        print(self.nodeList[f].__str__(), ". With weight: ", weight)
        
    def getNodes(self):
        # Returns all node keys in the list
        return self.nodeList.keys()

    def getNumberOfNodes(self):
        return self.numNodes