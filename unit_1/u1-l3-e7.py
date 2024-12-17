"""
Write a WeightedEdge class that extends Edge. Its constructor requires a 
weight parameter, as well as the parameters from Edge. You should additionally 
include a getWeight method. The string value of a WeightedEdge from node A to 
B with a weight of 3 should be "A->B (3)".
"""


class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name
    def getName(self):
        return self.nameß
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()
    

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight):
        # Your code here
        self.src = src
        self.dest = dest
        # Edge.__init__(self, src, dest)
        self.weight = weight
    def getWeight(self):
        # Your code here
        return self.weight
    def __str__(self):
        # Your code here
        return self.src.getName() + "->" + self.dest.getName() + " (" + str(self.weight) + ")" 
        # return Edge.__str__(self) + " (" + str(self.weight) + ")"
    
    
# Test   
 
print(WeightedEdge(Node("ABC"), Node("ACB"), 10))
