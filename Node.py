import math

class Node:
    def __init__(self, id):
        self.id = id
        self.inputSum = 0
        self.output = 0
        self.connections = []
        self.layer = 0
        self.drawPos = []
    def activate(self):
        if self.layer != 0:
            self.output = sigmoid(self.inputSum)
        for connection in self.connections:
            if connection.enabled:
                connection.toNode.inputSum += connection.weight * self.output
    def connected(self, otherNode):
        if otherNode.layer == self.layer:
            return False
        for n in otherNode.connections:
            if n.toNode == self or n.fromNode == self:
                return True
    def clone(self):
        n = Node(self.id)
        n.layer = self.layer
        return n
def stepFunction(x):
    if x < 0:
        return 0
    return 1
def relu(x):
    return max(0, x)
def sigmoid(x):
    return 1.0 / (1 + pow(math.e, -4.9*x))