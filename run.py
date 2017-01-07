from PIL import Image as im 
from imageHelper import * 
from fitness import *                                                                                                                                                                                        
import numpy as np
import sys, os, random, operator
 
def main(args):
    
    """
        Setup algorithm information
    """
    images = loadImagesToMemory()
    Individual.allImages = images        
    reference = loadReferenceAsTiles(args[1], 25)
    """
         Run
    """
    if(args[2] == "genetic"):
        genetic(images, reference, False)
    else:
        basic(images, reference, False)
    
"""
    The genetic version of the algorithm.
    Evolve for the best match.
"""    
def genetic(images, reference, replace):
    
    """
       Seed the initial random population.
    """
    populationNumber = 30
    population = []
    for n in range(0,populationNumber):
        tiles = []
        labels = []
        for x in range(0,len(reference.tiles)):
            tiles.append([])
            labels.append([])
            for y in range(0,len(reference.tiles[x])):
                s = str(hex(random.randint(1, len(images)-1)))
                labels[x].append(s)
                tiles[x].append(images[s])
        i = Individual(tiles,1)
        i.labels = labels
        population.append(i)
        
    Individual.replace = replace
        
    outputFile = "out/testResults.txt"
    numOfTiles = len(reference.tiles) * len(reference.tiles[0])
    writeInfo(outputFile, "Number of tiles : " + str(numOfTiles))    
    
    """
        Sort by fitness, smaller is better.
    """  
    for n in range(0,populationNumber):
        population[n].evaluateFitness(reference)
    population.sort(key=operator.attrgetter('fitnessTotal'))
    
    """
       Now run the actual genetic algorithm.
       Currently using a fixed iteration number vs an actual fitness score metric
    """
    for n in range(0, 2000):
        newPopulation = []
        for n1 in range(0,7):
           newPopulation.append(population[0].crossover(population[random.randint(0, len(population)-1)],reference,True))
        for n1 in range(0,6):
            newPopulation.append(population[1].crossover(population[random.randint(0, len(population)-1)],reference,True))
        for n1 in range(0,5):
           newPopulation.append(population[2].crossover(population[random.randint(0, len(population)-1)],reference,True))
        for n1 in range(0,4):
            newPopulation.append(population[3].crossover(population[random.randint(0, len(population)-1)],reference,True))
        for n1 in range(0,4):
            newPopulation.append(population[4].crossover(population[random.randint(0, len(population)-1)],reference,True))
         
        population.sort(key=operator.attrgetter('fitnessTotal'))
        population[0].show()
        writeRes(outputFile, population[0].fitnessTotal/float(numOfTiles))
        population = newPopulation[:populationNumber-5]
        
        # generate 5 new members for mutation purposes
        for n in range(0,5):
            tiles = []
            for x in range(0,len(reference.tiles)):
                tiles.append([])
                for y in range(0,len(reference.tiles[x])):
                    tiles[x].append(images[str(hex(random.randint(1, len(images)-1)))])
            i = Individual(tiles,1)
            i.evaluateFitness(reference)
            population.append(i)
            
    """
        Finalize the population
    """
    for n in range(0, 5):
        newPopulation = []
        for n1 in range(0,10):
            newPopulation.append(population[0].crossover(population[random.randint(0, len(population)-1)],reference,False))
        for n1 in range(0,10):
            newPopulation.append(population[1].crossover(population[random.randint(0, len(population)-1)],reference,False))
        for n1 in range(0,10):
           newPopulation.append(population[2].crossover(population[random.randint(0, len(population)-1)],reference,False))
        population.sort(key=operator.attrgetter('fitnessTotal'))
        population[0].show()
        writeRes(outputFile, population[0].fitnessTotal/float(numOfTiles))
        population = newPopulation[:populationNumber]
                
        
"""
    The 'dumb' version of the algorithm.
    Simply look for the best match.
"""
def basic(images, reference, replace):
    i = Individual([],-1)
    for x in range(0,len(reference.tiles)):
        i.tiles.append([])
        for y in range(0,len(reference.tiles[0])):
            i.tiles[x].append(getBestMatch(images,reference.tiles[x][y],replace))   
    i.evaluateFitnessAsNum(reference) 
    i.show()
    print(i.fitnessTotal/float(len(reference.tiles) * len(reference.tiles[0])))

if __name__ == "__main__":
  sys.exit(main(sys.argv))
