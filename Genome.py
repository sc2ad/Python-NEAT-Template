from Node import Node
from Connection import Connection
import ConnectionHistory
import random

WEIGHT_MUTATION_CHANCE = 0
ADD_CONNECTION_CHANCE = 0
ADD_NODE_CHANCE = 0

def initialize(weight_mutation_chance, add_connection_chance, add_node_chance):
    global WEIGHT_MUTATION_CHANCE, ADD_CONNECTION_CHANCE, ADD_NODE_CHANCE
    WEIGHT_MUTATION_CHANCE = weight_mutation_chance
    ADD_CONNECTION_CHANCE = add_connection_chance
    ADD_NODE_CHANCE = add_node_chance

class Genome:
    def __init__(self, inputs, outputs, crossover):
        assert WEIGHT_MUTATION_CHANCE * ADD_CONNECTION_CHANCE * ADD_NODE_CHANCE != 0, "You must call the initialize method before creating a Genome"
        self.genes = []
        self.nodes = []
        self.inputs = inputs
        self.outputs = outputs
        self.layers = 2
        self.nextNode = 0
        self.network = []
        self.biasNode = None
        if not crossover:
            self.setup()
    def setup(self):
        for i in range(self.inputs):
            temp = Node(i)
            temp.layer = 0
            self.nodes.append(temp)
            self.nextNode += 1
        for i in range(self.outputs):
            temp = Node(i + self.inputs)
            temp.layer = 1
            self.nodes.append(temp)
            self.nextNode += 1
        self.biasNode = Node(self.nextNode)
        self.biasNode.layer = 0
        self.nodes.append(self.biasNode)
        self.nextNode += 1
    def getNode(self, nodeId):
        for n in self.nodes:
            if n.id == nodeId:
                return n
        return None
    def connect(self):
        for n in self.nodes:
            n.connections = []
        for g in self.genes:
            g.fromNode.connections.append(g)
    def feedforward(self, input):
        assert self.network != None, "Need to create the network before using it"
        assert len(input) == self.inputs

        for i in range(self.inputs):
            self.nodes[i].output = input[i]
        self.biasNode.output = 1

        for n in self.network:
            n.activate()
        
        outs = []
        for i in range(self.outputs):
            outs.append(self.nodes[self.inputs + i].output)
        
        for n in self.nodes:
            n.inputSum = 0
        return outs
    def generateNetwork(self):
        self.connect()
        self.network = []

        for l in range(self.layers):
            for n in self.nodes:
                if n.layer == l:
                    self.network.append(n)
    def addNode(self, innovationHistory):
        if len(self.genes) == 0:
            self.addConnection(innovationHistory)
            return None
        rand = random.randint(0, len(self.genes)-1)
        temp = self.genes[rand]
        while temp.fromNode == self.biasNode and len(self.genes) != 1:
            temp = self.genes[random.randint(0, len(self.genes)-1)]
        
        temp.enabled = False
        toAdd = Node(self.nextNode)
        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, toAdd, temp.toNode)

        self.genes.append(Connection(temp.fromNode, toAdd, 1, connectionInnovationNumber))
        toAdd.layer = temp.fromNode.layer + 1

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.biasNode, toAdd)

        self.genes.append(Connection(self.biasNode, toAdd, 0, connectionInnovationNumber))

        if toAdd.layer == temp.toNode.layer:
            for n in self.nodes:
                if n.layer >= toAdd.layer:
                    n.layer += 1
            self.layers += 1
        
        self.nodes.append(toAdd)
        self.connect()
    def addConnection(self, innovationHistory):
        if self.fullyConnected():
            return None
        random1 = random.randint(0, len(self.nodes)-1)
        random2 = random.randint(0, len(self.nodes)-1)

        while self.isNonUnique(random1, random2):
            random1 = random.randint(0, len(self.nodes)-1)
            random2 = random.randint(0, len(self.nodes)-1)
    def isNonUnique(self, option1, option2):
        n1 = self.nodes[option1]
        n2 = self.nodes[option2]
        return n1.layer == n2.layer or n1.connected(n2)
    def getInnovationNumber(self, innovationHistory, fromNode, toNode):
        assert fromNode != None and toNode != None

        isNew = True
        connectionInnovationNumber = ConnectionHistory.nextConnectionInnovationNumber
        for h in innovationHistory:
            if h.matches(self, fromNode, toNode):
                isNew = False
                connectionInnovationNumber = h.innovation
                break
        
        if isNew:
            currentState = []
            for g in self.genes:
                currentState.append(g.innovation)
            
            innovationHistory.append(ConnectionHistory.ConnectionHistory(fromNode.id, toNode.id, connectionInnovationNumber, currentState))
            ConnectionHistory.nextConnectionInnovationNumber += 1
        return connectionInnovationNumber
    def fullyConnected(self):
        maxConnections = 0
        layeredNodes = [0] * self.layers
        for n in self.nodes:
            layeredNodes[n.layer] += 1
        for i in range(self.layers-1):
            nodesInFront = 0
            for j in range(i+1,self.layers):
                nodesInFront += layeredNodes[j]
            maxConnections += layeredNodes[i] * nodesInFront
        
        if maxConnections == len(self.genes):
            return True
        return False
    def mutate(self, innovationHistory):
        if not len(self.genes):
            self.addConnection(innovationHistory)
        if random.random() < WEIGHT_MUTATION_CHANCE:
            for g in self.genes:
                g.mutateWeight()
        if random.random() < ADD_CONNECTION_CHANCE:
            self.addConnection(innovationHistory)
        if random.random() < ADD_NODE_CHANCE:
            self.addNode(innovationHistory)
    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)

        child.genes = []
        child.nodes = []
        child.layers = self.layers
        child.nextNode = self.nextNode
        child.biasNode = self.biasNode
        childGenes = []
        enabled = []
        for g in self.genes:
            setEnabled = True
            p2gene = parent2.matchingGene(g.innovation)
            if p2gene != -1:
                g2 = parent2.genes[p2gene]
                if not g.enabled or not g2.enabled:
                    if random.random() < 0.75:
                        setEnabled = False
                if random.random() < 0.5:
                    childGenes.append(g)
                else:
                    childGenes.append(g2)
            else:
                childGenes.append(g)
                setEnabled = g.enabled
            enabled.append(setEnabled)
        
        for n in self.nodes:
            child.nodes.append(n.clone())
        for i in range(len(childGenes)):
            g = childGenes[i]
            child.genes.append(g.clone(child.getNode(g.fromNode.id), child.getNode(g.toNode.id)))
            g.enabled = enabled[i]
        child.biasNode = child.getNode(child.biasNode)
        child.connect()
        return child
    def matchingGene(self, innovation):
        for i in range(len(self.genes)):
            if self.genes[i].innovation == innovation:
                return i
        return -1
    def clone(self):
        clone = Genome(self.inputs, self.outputs, True)

        for n in self.nodes:
            clone.nodes.append(n)
        for g in self.genes:
            clone.genes.append(g.clone(clone.getNode(g.fromNode.id), clone.getNode(g.toNode.id)))
        
        clone.layers = self.layers
        clone.nextNode = self.nextNode
        clone.biasNode = self.biasNode.clone()
        clone.connect()
        clone.generateNetwork()

        return clone
