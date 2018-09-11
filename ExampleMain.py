from Population import Population, load, save
from Population import initialize as init_pop
from Player import Player
from Player import initialize as init_player
from Genome import initialize as init_genome
from Connection import initialize as init_connection

populationSize = 500
gens = 10
checkpoint_frequency = 2
saveFile = "test.pkl"
inputs, outputs = 1,2
weight, connection, node = 0.7, 0.4, 0.1
re_randomize = 0.4

# Must be in this order!
init_connection(re_randomize)
init_genome(weight, connection, node)
init_player(inputs, outputs)

pop = Population(populationSize)
for i in range(gens):
    print("Starting generation: "+str(i))
    while not pop.done():
        # This assumes that the population eventually dies
        pop.updateAlive()
        currentPlayer = pop.getCurrentPlayer()
        if currentPlayer.dead:
            if currentPlayer.fitness > pop.bestFitness:
                pop.bestFitness = currentPlayer.fitness
                pop.bestPlayer = currentPlayer.cloneForReplay()
            pop.currentIndex += 1
    if i % checkpoint_frequency == 0:
        save(pop, saveFile)
    pop.naturalSelection()
