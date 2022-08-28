from node import Node

class Graph:
    def __init__(self):
        self.nodeList = {}
        self.numNodes = 0
    
    def addNode(self,line,col,model):
        self.numNodes += 1
        newNode = Node(self.line, self.col, self.model)
        self.nodeList[newNode.id] = newNode # Adds the new node to the node list
        
        return newNode
      
    def getNode(self, id):
        """
        If vertex with key is in Graph then return the Vertex
        Time complexity is O(1) as we are simply checking whether
        the key exists or not in a dictionary and returning it
        """
        
        #use the get method to return the Vertex if it exists
        #otherwise it will return None
        return self.nodeList.get(id)
      
    def __contains__(self, key):
        """
        Check whether vertex with key is in the Graph
        Time complexity is O(1) as we are simply checking whether 
        the key is in in the dictrionary or not
        """
        
        #returns True or False depending if in list
        return key in self.nodeList
      
    def addEdge(self, f, t, weight = 0):
        """
        Add an edge to connect two vertices of t and f with weight
        assuming directed graph
        
        Time complexity of O(1) as adding vertices if they don't 
        exist and then add neighbor
        """
        
        #add vertices if they do not exist
        if f not in self.nodeList:
            nv = self.addNode(f)
        if t not in self.nodeList:
            nv = self.addNode(t)
            
        #then add Neighbor from f to t with weight
        self.nodeList[f].addNeighbor(self.nodeList[t], weight)
        
    def getNodes(self):
        """
        Return all the vertices in the graph
        Time complexity is O(1) as we simply return all the keys
        in the nodeList dictionary
        """
       
        return self.nodeList.keys()
      
    def getCount(self):
        """
        Return a count of all vertices in the Graph
       
        Time complexity O(1) because we just return the count
        attribute
        """
        return self.numNodes