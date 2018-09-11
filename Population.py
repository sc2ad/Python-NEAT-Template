from Species import Species
import pickle
from Player import Player

EXTINCTION_SAVE_TOP = 0
def initialize(save_top):
    global EXTINCTION_SAVE_TOP
    EXTINCTION_SAVE_TOP = save_top

class Population:
    def __init__(self, size):
        self.pop = []
        self.bestPlayer = None
        self.bestFitness = 0
        self.gen = 0
        self.innovationHistory = []
        self.generationPlayers = []
        self.species = []
        self.massExtinction = False
        self.currentIndex = 0

        for i in range(size):
            player = Player()
            player.brain.generateNetwork()
            player.brain.mutate(self.innovationHistory)
            self.pop.append(player)
    def updateAlive(self):
        if self.currentIndex < len(self.pop):
            self.pop[self.currentIndex].update()

    def getCurrentPlayer(self):
        if self.currentIndex < len(self.pop):
            return self.pop[self.currentIndex]
        return None
    
    def done(self):
        for p in self.pop:
            if not p.dead:
                return False
        return True

    def setBestPlayer(self):
        tempBest = self.species[0].players[0]
        tempBest.gen = self.gen
        if tempBest.fitness >= self.bestFitness:
            self.generationPlayers.append(tempBest.cloneForReplay())
            self.bestFitness = tempBest.fitness
            self.bestPlayer = tempBest.cloneForReplay()
    
    def naturalSelection(self):
        self.speciate()
        self.calculateFitness()
        self.sortSpecies()
        if self.massExtinction:
            self.massExtinctionEvent()
            massExtinction = False
        self.cullSpecies()
        self.setBestPlayer()
        self.killStaleSpecies()
        self.killBadSpecies()

        averageSum = self.getAvgFitnessSum()

        children = []
        for s in self.species:
            c = s.champ.cloneForReplay()
            c.speciesName = s.name
            children.append(c)

            childrenCount = s.averageFitness * len(self.pop) // averageSum - 1
            for i in range(childrenCount):
                temp = s.getOffspring(self.innovationHistory)
                temp.gen = self.gen
                children.append(temp)
        while len(children) < len(self.pop):
            temp = self.species[0].getOffspring(self.innovationHistory)
            temp.speciesName = self.species[0].name
            temp.gen = self.gen
            children.append(temp)
        
        self.pop = []
        self.pop = children.copy()
        self.gen += 1
        for p in self.pop:
            p.brain.generateNetwork()
        self.currentIndex = 0
    
    def speciate(self):
        for s in self.species:
            s.players = []
        for p in self.pop:
            speciesFound = False
            for s in self.species:
                if s.sameSpecies(p.brain):
                    s.addToSpecies(p)
                    speciesFound = True
                    break
            if not speciesFound:
                self.species.append(Species(p))

    def calculateFitness(self):
        for i in range(1,len(self.pop)):
            self.pop[i].calculateFitness()
    
    def sortSpecies(self):
        for s in self.species:
            s.sortSpecies()
        # This can also be done with quick sort or merge sort
        temp = []
        for i in [0] * len(self.species):
            m = 0
            maxI = 0
            for j in range(len(self.species)):
                if self.species[j].bestFitness > m:
                    m = self.species[j].bestFitness
                    maxI = j
            temp.append(self.species[j])
            del(self.species[maxI])
    
    def killStaleSpecies(self):
        for i in [2] * (len(self.species) - 2):
            if self.species[i].staleness >= 15:
                del(self.species[i])

    def killBadSpecies(self):
        averageSum = self.getAvgFitnessSum()

        for i in [1] * (len(self.species) - 1):
            if self.species[i].averageFitness / averageSum * len(self.species[i].players) < 1:
                del(self.species[i])
    
    def getAvgFitnessSum(self):
        averageSum = 0
        for s in self.species:
            averageSum += s.averageFitness
        return averageSum
    
    def cullSpecies(self):
        for s in self.species:
            s.cull()
            s.fitnessSharing()
            s.setAverage()
    
    def massExtinctionEvent(self):
        for i in [EXTINCTION_SAVE_TOP-1] * (len(self.species) - (EXTINCTION_SAVE_TOP-1)):
            del(self.species[i])

def save(population, filename):
    pickle.dump(population, filename)
def load(filename):
    return pickle.load(filename)