#physic.py
import random
import pygame

def freeFall(time_after,start_y):
    return int((start_y + (9.81* time_after * time_after / 100000)))

def getRandBool(chanceTrue = 50):
    return (random.randrange(100)<chanceTrue)

def get_collideDir(spriteA,spriteB):
    #0:no collide,1:up,2:down,3:left,4:right,5:inside or error
    if spriteB.rect.bottom <= (spriteA.rect.top + 2):
        return 1
    elif spriteB.rect.top >= (spriteA.rect.bottom - 2):
        return 2
    elif spriteB.rect.right <= (spriteA.rect.left + 2):
        return 3
    elif spriteB.rect.left >= (spriteA.rect.right - 2):
        return 4
    else:
        return 5

        
        
        
    
    
