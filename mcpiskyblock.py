from mcpi.minecraft import Minecraft
import random
from random import randrange
import time
mc = Minecraft.create()
from perlin_noise import PerlinNoise
mc.setBlocks(-256, -64, -256, 256, 128, 256, 0)
seedinput = input('insert seed here (must be an integer): ')

try:
    random.seed(seedinput)
except:
    random.seed()
islandcount = randrange(10,50)
worldseed = randrange(-99999999,99999999)
heightseed = randrange(-99999999,99999999)
noise = PerlinNoise(octaves=2, seed=int(seedinput))
world = PerlinNoise(octaves=.1, seed=int(worldseed))
heightmap = PerlinNoise(octaves=.1, seed=int(heightseed))
plantsmap = PerlinNoise(octaves=10, seed=int(heightseed))
def tree(x,y,z,biome):
    treeheight = randrange(3,5)
    
    mc.setBlocks(x-1,y+treeheight,z-1,x+1,y+treeheight+1,z+1,18)
    mc.setBlocks(x-2,y+treeheight-1,z-2,x+2,y+treeheight-2,z+2,18)
    mc.setBlocks(x,y,z,x,y+treeheight,z,17)
    
def genisland(x,z,biome,size,height):
    freq=24
    amp = 10
    
    if biome == "plain":
        for x1 in range(size):
            for z1 in range(size):
                finalx = x1 + x
                finalz = z1 + z
                
                heightblock = round(world([finalx/freq,finalz/freq])*8)
                heightmapblock = round(world([finalx/15,finalz/15])*300)
                y1 = noise([finalx/freq,finalz/freq]) * heightmapblock
                ynoheight = noise([finalx/freq,finalz/freq])
                #print(heightblock)
                

                if heightblock == 1:
                    #stone
                    mc.setBlocks(finalx,y1,finalz,finalx,height,finalz,1)
                    #dirt
                    mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,13)
                elif heightblock ==-1:
                    #stone
                    mc.setBlocks(finalx,y1,finalz,finalx,height,finalz,1)
                    #dirt
                    mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,12)
                elif heightblock == 2:
                    #stone
                    mc.setBlocks(finalx,y1,finalz,finalx,height,finalz,1)
                    #dirt
                    mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,1)
                    #grass
                    mc.setBlock(finalx,y1,finalz,1)
                else:
                    #tree/plants
                    plants = round(plantsmap([finalx/freq,finalz/freq])*100)
                    
                    if plants == 2:
                        tree(finalx,y1+1,finalz,"plains")
                        
                    #stone
                    mc.setBlocks(finalx,y1,finalz,finalx,height,finalz,1)
                    #dirt
                    mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,3)
                    #grass
                    mc.setBlock(finalx,y1,finalz,2)
genisland(0,0,"plain",8,-15)
#tree(0,0,0,"plains")
for a in range(islandcount):
    print(f'generated {a} out of {islandcount}')
    genisland(randrange(-128,128),randrange(-128,128),"plain",randrange(5,18),-7)
    time.sleep(.5)