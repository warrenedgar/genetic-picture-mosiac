from PIL import Image as im
import numpy as np
import sys, os
counter = 1;
os.system("mkdir -p ../tiles")
qv = 95

# for every file in the directory
#   if image
#     chop it to a square, scale it and save it
for filename in os.listdir('.'):
  if '.jpg' in filename or '.png' in filename:
    image = im.open(filename)
    xsize, ysize = image.size
    if(xsize < ysize):
      image = image.crop((0,0,xsize,xsize))
      image = image.resize((100,100),im.ANTIALIAS)
      image.save('../tiles/' + hex(counter)+'.jpg','JPEG',quality=qv)
      counter += 1
    else:
      image = image.crop((0,0,ysize,ysize))
      image = image.resize((100,100),im.ANTIALIAS)
      image.save('../tiles/' + hex(counter)+'.jpg','JPEG',quality=qv)
      counter += 1
print(counter , " tiles made")
