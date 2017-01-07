from PIL import Image
import sys, random
from fitness import *                                                                                                                                                                                        

"""
" class that represents an Indivdual within
" the popluation
"
" its actually modeling a tiled image for this
" project
"""
class Individual:
    
    # will hold a ref to the dict of all images
    allImages = 0 
    
    # use image once or as many times as possible
    replace = False;
    
    """
       Setup the initial individual, generation and fitness simply won't be used
       for the best match algorithm.
    """
    def __init__(self, tiles, generation):
        self.tiles = tiles
        self.generation = generation
        self.fitnessTotal = sys.maxint
        self.fitness = []
        self.labels = []
        for x in range(0, len(self.tiles)):
            self.fitness.append([])
            self.labels.append([])
            for y in range(0, len(self.tiles[x])):
                self.fitness[x].append(sys.maxint)
                self.labels[x].append(str(sys.maxint))
    
    """
       Mehod for debugging/saving image.
    """   
    def show(self):
        width = len(self.tiles)
        height = len(self.tiles[0])
        image = Image.new('RGB', (width * 25,height * 25))
        for x in range(0, width):
            for y in range(0, height):
                image.paste(self.tiles[x][y],(x*25,y*25,(x+1)*25,(y+1)*25))
        #image.show()
        image.save('out/' + str(self.generation).zfill(3) + 'result.jpg','JPEG',quality=95)
    
    """
        Method is called to evaulate fitness, originally.
        Is done later by the crossover to save operation counts.
    """
    def evaluateFitness(self, reference):
        self.fitnessTotal = 0
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[x])):
                result = mse(self.tiles[x][y],reference.tiles[x][y])
                self.fitness[x][y] = result
                self.fitnessTotal += result
                
    """
        Method is called to evaulate fitness,
        just saves as number.
    """
    def evaluateFitnessAsNum(self, reference):
        self.fitnessTotal = 0
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[x])):
                self.fitnessTotal += mse(self.tiles[x][y],reference.tiles[x][y])
                
    """
        Method to test if tile is already present
    """
    def hasLabel(self, label):
        for x in range(0, len(self.tiles)):
            for y in range(0, len(self.tiles[x])):
                self.fitnessTotal += mse(self.tiles[x][y],reference.tiles[x][y])
                
        return False
        
    """
       This is essentialy breeding the two members of the population togeather.
       Note that mutation is being called during this operation.         
    """
    def crossover(self, other, reference, change):
        if Individual.replace == True:
            return self.crossoverReplace(other, reference, change)
        width = len(self.tiles)
        height = len(self.tiles[0])
        newFit = 0.0;
        tiles = []
        fitness = []
        labels = []
        for x in range(0, width):
            tiles.append([])
            fitness.append([])
            for y in range(0, height):
                left = mse(self.tiles[x][y],reference.tiles[x][y])
                right = mse(other.tiles[x][y],reference.tiles[x][y])
                if(self.fitness[x][y] < other.fitness[x][y]):
                    tiles[x].append(self.mutate(self.tiles[x][y],change))
                    fitness[x].append(left)
                    labels[x].append(self.labels[x][y])
                    newFit += left
                else:
                    tiles[x].append(self.mutate(other.tiles[x][y],change))
                    fitness[x].append(right)
                    newFit += right
        i = Individual(tiles, self.generation + 1)
        i.fitnessTotal = newFit
        i.fitness = fitness
        return i
        
    """
       This is essentialy breeding the two members of the population togeather.
       Note this is more complicated then above simply because we must keep
       track of the unique tiles in every image.
    """
    def crossoverReplace(self, other, reference, change):
        width = len(self.tiles)
        height = len(self.tiles[0])
        newFit = 0.0;
        tiles = []
        fitness = []
        labels = []
        lHash = {}
        for x in range(0, width):
            tiles.append([])
            fitness.append([])
            labels.append([])
            for y in range(0, height):
                left = mse(self.tiles[x][y],reference.tiles[x][y])
                right = mse(other.tiles[x][y],reference.tiles[x][y])
                if(self.fitness[x][y] < other.fitness[x][y]):
                    key = self.labels[x][y]
                    if key in lHash:
                        newKey = str(hex(random.randint(1, len(Individual.allImages)-1)))
                        while newKey in lHash:
                            newKey = str(hex(random.randint(1, len(Individual.allImages)-1)))
                        tiles[x].append(self.mutate(Individual.allImages[newKey],change))
                        lHash[newKey] = 1
                        l = mse(Individual.allImages[newKey],reference.tiles[x][y])
                        fitness[x].append(l)
                        newFit += l
                        labels[x].append(newKey)
                    else:
                        labels[x].append(key)
                        lHash[key] = 1
                        newFit += left
                        tiles[x].append(self.mutate(self.tiles[x][y],change))
                        fitness[x].append(left)
                else:
                    key = other.labels[x][y]
                    if key in lHash:
                        newKey = str(hex(random.randint(1, len(Individual.allImages)-1)))
                        while newKey in lHash:
                            newKey = str(hex(random.randint(1, len(Individual.allImages)-1)))
                        tiles[x].append(self.mutate(Individual.allImages[newKey],change))
                        lHash[newKey] = 1
                        r = mse(Individual.allImages[newKey],reference.tiles[x][y])
                        fitness[x].append(r)
                        newFit += r
                        labels[x].append(newKey)
                    else:
                        labels[x].append(key)
                        lHash[key] = 1
                        newFit += right
                        tiles[x].append(self.mutate(other.tiles[x][y],change))
                        fitness[x].append(right)
                        
        i = Individual(tiles, self.generation + 1)
        i.fitnessTotal = newFit
        i.fitness = fitness
        i.labels = labels
        return i
       
    """
       The mutation for an individual is that is a probability a tile
       will be switched out with a new random tile
    """ 
    def mutate(self, img, change):
        #if random.random() < .05 and change == True:
        #    img = Individual.allImages[str(hex(random.randint(1, len(Individual.allImages)-1)))]
        return img
