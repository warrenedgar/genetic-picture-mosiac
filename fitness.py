from PIL import Image, ImageChops
import numpy as np
import sys, os, math
 
"""
   Works!
   be measuring the spread of color it gives a more accurate, and
   prevents the above problem. 
   Code adapted from here ->
   http://code.activestate.com/recipes/577630-comparing-two-images/
"""   
def mse(img1,img2):
    rms = sys.maxint
    try:
        diff = ImageChops.difference(img1, img2)
        h = diff.histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        rms = math.sqrt(sum(sq)/float(img1.size[0] * img1.size[1]))
    finally:
        return rms
