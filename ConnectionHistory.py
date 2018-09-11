class ConnectionHistory:
    def __init__(self, fromNodeId, toNodeId, innovation, originalGenome):
        self.fromNode = fromNodeId
        self.toNode = toNodeId
        self.innovation = innovation
        self.originalGenome = originalGenome
    def matches(self, genome, fromNode, toNode):
        if len(genome.genes) == len(self.originalGenome):
            if fromNode.id == self.fromNode and toNode.id == self.toNode:
                for gene in genome.genes:
                    if not gene.innovation in self.originalGenome:
                        return False
                return True
        return False
nextConnectionInnovationNumber = 0