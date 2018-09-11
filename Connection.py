import random
import numpy as np

RE_RANDOMIZE_WEIGHT_CHANCE = 0
def initialize(randomize_weight):
    global RE_RANDOMIZE_WEIGHT_CHANCE
    RE_RANDOMIZE_WEIGHT_CHANCE = randomize_weight

class Connection:
    def __init__(self, fromNode, toNode, weight, innovation):
        assert RE_RANDOMIZE_WEIGHT_CHANCE != 0, "Must call the initialize function before making a class"
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = weight
        self.innovation = innovation
        self.enabled = True
    def mutateWeight(self):
        rand = random.random()
        if rand < RE_RANDOMIZE_WEIGHT_CHANCE:
            weight = random.random() * 2 - 1
        else:
            weight /= 1 - random.random()
    def clone(self):
        con = Connection(self.fromNode, self.toNode, self.weight, self.innovation)
        con.enabled = self.enabled
        return con