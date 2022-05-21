try:
    from mcpi.minecraft import Minecraft
except:
    warn("The mcpi library was not found")
    exit()
import random
from random import randrange
import time
from log import *
try:
    from perlin_noise import PerlinNoise
except:
    warn("perlin_noise was not found")
    import os
    os.system("pip install perlin_noise")
    log("Start the script again")
    exit()
try:
    mc = Minecraft.create()
except ConnectionRefusedError:
    crit("No mcpi process was found, start mcpi and open a world")
    exit()

mc.setBlocks(-256, -64, -256, 256, 128, 256, 0)
info("Type the seed")
seedinput = input("")

try:
    random.seed(seedinput)
except:
    warn("No seed given, generating a random one.")
    random.seed()
islandcount = randrange(50,75)
worldseed = randrange(-99999999,99999999)
heightseed = randrange(-99999999,99999999)
noise = PerlinNoise(octaves=2, seed=int(seedinput))
world = PerlinNoise(octaves=.1, seed=int(worldseed))
heightmap = PerlinNoise(octaves=.1, seed=int(heightseed))
plantsmap = PerlinNoise(octaves=10, seed=int(heightseed))
ores = PerlinNoise(octaves=15, seed=int(seedinput))
def tree(x,y,z,biome):
    treeheight = randrange(3,5)
    if biome == "plains":
        mc.setBlocks(x-1,y+treeheight,z-1,x+1,y+treeheight+1,z+1,18)
        mc.setBlocks(x-2,y+treeheight-1,z-2,x+2,y+treeheight-2,z+2,18)
        mc.setBlocks(x,y,z,x,y+treeheight,z,17)
    if biome == "desert":
        mc.setBlocks(x,y,z,x,y+treeheight,z,81)
    if biome == "taiga":
        taigaheight = treeheight*2
        #tippy top
        mc.setBlock(x,y+taigaheight+1,z,18,1)
        #topshort
        mc.setBlocks(x-1,y+taigaheight,z,x+1,y+taigaheight,z,18,1)
        mc.setBlocks(x,y+taigaheight,z+1,x,y+taigaheight,z-1,18,1)
        #middleshort
        mc.setBlocks(x-1,y+taigaheight-2,z,x+1,y+taigaheight-2,z,18,1)
        mc.setBlocks(x,y+taigaheight-2,z+1,x,y+taigaheight-2,z-1,18,1)
        #bottomshort
        mc.setBlocks(x-1,y+taigaheight-4,z,x+1,y+taigaheight-4,z,18,1)
        mc.setBlocks(x,y+taigaheight-4,z+1,x,y+taigaheight-4,z-1,18,1)
        #topbig
        mc.setBlocks(x-2,y+taigaheight-3,z+1,x+2,y+taigaheight-3,z-1,18,1)
        mc.setBlocks(x+1,y+taigaheight-3,z+2,x-1,y+taigaheight-3,z-2,18,1)   
        #bottombig
        mc.setBlocks(x-2,y+taigaheight-5,z+1,x+2,y+taigaheight-5,z-1,18,1)
        mc.setBlocks(x+1,y+taigaheight-5,z+2,x-1,y+taigaheight-5,z-2,18,1)                    
        #mc.setBlocks(x-1,y+treeheight,z-1,x+1,y+treeheight+5,z+1,18,1)
        #mc.setBlocks(x-2,y+treeheight-1,z-2,x+2,y+treeheight,z+2,18,1)
        mc.setBlocks(x,y,z,x,y+taigaheight,z,17,1)
    if biome =="nether":
        mc.setBlock(x,y,z,10)
        
def oregen(x,y,z,var):
    height = randrange(0,3)
    
    if var == 1:
        mc.setBlocks(x,y,z,x,y-height,z,16)
        #print("gen ore")
    if var == 2:
        mc.setBlocks(x,y,z,x,y-height,z,15)
    if var == 3:
        mc.setBlocks(x,y,z,x+height/2,y-height,z,14)
    if var == -4:
        mc.setBlocks(x,y,z,x,y-height/2,z,56)
    if var == 10:
        mc.setBlocks(x,y,z,x,y-height,z,13)
def genisland(x,z,size,height):
    freq=24
    amp = 10
    
    
    for x1 in range(size):
        for z1 in range(size):
            finalx = x1 + x
            finalz = z1 + z
            ore = round(ores([finalx/freq,finalz/freq])*10)
            #print(ore)
            heightblock = round(world([finalx/freq,finalz/freq])*16)
            heightmapblock = round(world([finalx/15,finalz/15])*100)
            y1 = noise([finalx/freq,finalz/freq]) * heightmapblock
            ynoheight = noise([finalx/freq,finalz/freq])
            plants = round(plantsmap([finalx/freq,finalz/freq])*100)
            
            
            if heightblock == -4: # gravel patches
              
                #dirt
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,13)
                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,1)
                
                
            elif heightblock ==-1: #desert
             
                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,1)
                #sand
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,12)
                
                
                if plants == 2:
                    time.sleep(.3)
                    tree(finalx,y1+1,finalz,"desert")
                
            elif heightblock == -2: #mountains
                
                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,1)
                #dirt
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,1)
                #grass
                mc.setBlock(finalx,y1,finalz,1)
            elif heightblock == 2: #taiga
               
                if ore >=1:
                    mc.setBlock(finalx,y1+1,finalz,78)
                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,1)
                #dirt
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,1)
                #grass
                mc.setBlock(finalx,y1,finalz,80)
                if plants == 8:
                    tree(finalx,y1+1,finalz,"taiga")

            elif heightblock == -3: #nether

                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,87)
                #dirt
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,87)
                
                
                if plants == 2:
                    tree(finalx,y1+1,finalz,"nether")
                elif plants >=40:
                    mc.setBlock(finalx,y1+1,finalz,39)
                elif plants >=20:
                    mc.setBlock(finalx,y1+1,finalz,40)
                #ores
                oregen(finalx,y1+height+randrange(-5,7),finalz,10)
            else: #plains
                
                
                #tree/plants
                #stone
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height-5,finalz,1)
                #dirt
                mc.setBlocks(finalx,y1,finalz,finalx,y1+height/8,finalz,3)
                #grass
                mc.setBlock(finalx,y1,finalz,2)
                if plants == 2:
                    tree(finalx,y1+1,finalz,"plains")
                elif plants >=40:
                    mc.setBlock(finalx,y1+1,finalz,37)
                elif plants >=20:
                    mc.setBlock(finalx,y1+1,finalz,38)
            if not heightblock == -3:
                oregen(finalx,y1+height+randrange(-3,7),finalz,ore)
           
genisland(0,0,8,-15)
#tree(0,0,0,"plains")
for a in range(islandcount):
    finalcount = a / islandcount*100
    info(f'generated {round(finalcount)}%')
    
    genisland(randrange(-128,128),randrange(-128,128),randrange(5,18),-7)
    time.sleep(.5)
info(f'generated 100%')