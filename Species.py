import random
class Species:
    def __init__(self, player=None):
        self.players = []
        self.bestFitness = 0
        self.name = ""
        self.champ = None
        self.averageFitness = 0
        self.staleness = 0
        self.representative = None
        if player != None:
            player.speciesName = self.name
            self.players.append(player)
            self.bestFitness = player.fitness
            self.representative = player.brain.clone()
            self.champ = player.cloneForReplay()
    def sameSpecies(self, genome):
        compatibility = 0
        excessAndDisjoint = getExcessDisjoint(genome, self.representative)
        averageWeightDiff = getAverageWeightDiff(genome, self.representative)

        largeGenomeNormalizer = max(1, len(genome.genes) - 20)
        compatibility = (excessCoeff * excessAndDisjoint/largeGenomeNormalizer) + (weightDiffCoeff * averageWeightDiff)

        return compatibilityThreshold > compatibility
    def addToSpecies(self, player):
        self.players.append(player)
        player.speciesName = self.name
    def sortSpecies(self):
        temp = []
        # Should replace this with quicksort
        for i in range(len(self.players)):
            m = 0
            maxI = 0
            for j in [0] * len(self.players):
                if self.players[j].fitness > m:
                    m = self.players[j].fitness
                    maxI = j
            temp.append(self.players[m])
            del(self.players[maxI])
        if len(self.players) == 0:
            self.staleness = 200
            return None
        if self.players[0].fitness > self.bestFitness:
            self.staleness = 0
            self.bestFitness = self.players[0].fitness
            self.representative = self.players[0].brain.clone()
            self.champ = self.players[0].cloneForReplay()
        else:
            self.staleness += 1
    def setAverage(self):
        s = 0
        for p in self.players:
            s += p.fitness
        self.averageFitness = s / len(self.players)
    def getOffspring(self, innovationHistory):
        baby = None
        if random.random() < 0.25:
            baby = self.selectPlayer().clone()
        else:
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()

            if parent1.fitness >= parent2.fitness:
                baby = parent1.crossover(parent2)
            else:
                baby = parent2.crossover(parent1)
        baby.brain.mutate(innovationHistory)
        return baby
    def selectPlayer(self):
        fitnessSum = 0
        for p in self.players:
            fitnessSum += p.fitness
        
        rand = (1-random.random()) * fitnessSum
        runningSum = 0
        for p in self.players:
            runningSum += p.fitness
            if runningSum >= rand:
                return p
        return self.players[0]
    def cull(self):
        if len(self.players > 2):
            for i in [len(self.players) // 2] * (len(self.players)-len(self.players)//2):
                del(self.players[i])
    def fitnessSharing(self):
        for p in self.players:
            p.fitness /= len(self.players)

def getExcessDisjoint(genome1, genome2):
    matching = 0
    for g1 in genome1.genes:
        for g2 in genome2.genes:
            if g1.innovation == g2.innovation:
                matching += 1
                break
    return len(genome1.genes) + len(genome2.genes) - 2 * matching

def getAverageWeightDiff(genome1, genome2):
    if len(genome1.genes) == 0 or len(genome2.genes) == 0:
        return 0
    matching = 0
    totalDiff = 0
    for g1 in genome1.genes:
        for g2 in genome2.genes:
            if g1.innovation == g2.innovation:
                matching += 1
                totalDiff += abs(g1.weight - g2.weight)
                break
    if matching == 0:
        return 100000
    return totalDiff / matching

excessCoeff = 1
weightDiffCoeff = 0.5
compatibilityThreshold = 3