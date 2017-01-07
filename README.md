# genetic-picture-mosiac

This was done as an investigation into using genetic algorithms to create art. Please see the paper.pdf file for more information along with the pretty pictures.

The code in this directory isn't meant to be *run*, instead it serves as an accompaniment to the paper.
Depending on the size of your reference image it will take a while =).

However, if you want to run it for some reason, you would need an set of tiled images. After collecting all of the images you would like to use in the the tile set, run utilScripts/imageShear.py in the corresponding folder. Then move the newly made tiles directory to the same main folder.

```
 python2 run.py pathToTargetFile.jpg genetic
```
For the genetic version. The following will run the dumb dfs mentioned in the paper. 
```
 python2 run.py pathToTargetFile.jpg basic
```
