from Genome import Genome

INPUTS = 0
OUTPUTS = 0

def initialize(inputs, outputs):
    global INPUTS, OUTPUTS
    INPUTS, OUTPUTS = inputs, outputs

class Player:
    def __init__(self):
        assert INPUTS != 0 and OUTPUTS != 0, "You must call the initialize method before creating players!"
        self.fitness = -1
        self.unadjustedFitness = -1
        self.brain = Genome(INPUTS, OUTPUTS, False)
        self.vision = []
        self.actions = []
        self.lifespan = 0
        self.dead = False
        self.replay = False
        self.gen = 0
        self.name = ""
        self.speciesName = "Not yet defined"
    def update(self):
        # Does something that will eventually end up in death or victory
        # for the organism
        pass
    def look(self):
        # Looks at the input - This is where you should populate your vision
        # array
        pass
    def think(self):
        # Makes actions based off of input
        # Fill in based off of what you want to happen
        pass
    def clone(self):
        out = Player()
        out.replay = False
        out.fitness = self.fitness
        out.gen = self.gen
        out.brain = self.brain.clone()
        return out
    def cloneForReplay(self):
        out = Player()
        out.replay = True
        out.fitness = self.fitness
        out.brain = self.brain.clone()
        out.speciesName = self.speciesName
    def calculateFitness(self):
        # To return the calculated fitness at any given point in time
        pass
    def getFitness(self):
        if not self.replay:
            return self.calculateFitness()
        return self.fitness
    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child
    