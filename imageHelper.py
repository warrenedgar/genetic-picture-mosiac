from PIL import Image
from objects import *

"""
    Write Results to a file
"""
def writeInfo(filepath, info):
    with open(filepath, "a") as text_file:
        text_file.write(info + '\n')
        
def writeRes(filepath, num):
    with open(filepath, "a") as text_file:
        text_file.write(str(num) + '\n')

"""
   Load all the tiles into memory.
"""
def loadImagesToMemory():
    images = {}
    for filename in os.listdir('./tiles'):
      if '.jpg' in filename or '.png' in filename:
        temp = Image.open('./tiles/'+filename)
        images[filename.rsplit( ".", 1 )[ 0 ]] = temp.copy()
        temp.close()
    return images

"""
   From a set of images, get the best match.
   If using non-replace one, take out image after using it.
"""
def getBestMatch(images, ref, replace):
    best = ''
    last = 999999999
    removeKey = 'k'
    for key, value in images.iteritems():
        fitScore = mse(value,ref)
        if(fitScore < last):
            last = fitScore
            best = value
            removeKey = key
    if replace:
        del images[removeKey]
    return best

"""
   Given a file path, load the reference image.
   Then chop it up into tiles of a given size.
"""
def loadReferenceAsTiles(path, tileSize):
    image = Image.open(path)
    imgwidth, imgheight = image.size
    
    # cut the image to be tileable
    xMax = imgwidth/tileSize
    yMax = imgheight/tileSize
    image = image.crop((0,0,tileSize*xMax,tileSize*yMax))
    imgwidth, imgheight = image.size
    
    tiles = []
    
    # now create tiles
    for x in range(0,xMax):
        tiles.append([])
        for y in range(0,yMax):
            box = (x*tileSize, y*tileSize, (x+1)*tileSize, (y+1)*tileSize)
            tile = image.crop(box)
            tiles[x].append(tile)
    
    # make class
    i = Individual(tiles,1)
    return i

def makeRandom(allTiles):
    print("")