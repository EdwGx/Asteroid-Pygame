#physic.py
import random
import pygame

def freeFall(time_after,start_y):
    return int((start_y + (9.81* time_after * time_after / 100000)))

def number_collide(spriteA,spriteB,dokillA,dokillB):
    if spriteA.number == 0:
        if dokillA:
            spriteA.kill()
        return True
    if spriteB.number == 0:
        if dokillB:
            spriteB.kill()
        return False
    
    if ((spriteA.mu == False) and (spriteA.di == False)) and(
        (spriteB.mu == False) and (spriteB.di == False)):
            spriteA.number += spriteB.number
    elif spriteA.mu and spriteB.mu :
        spriteA.number = spriteA.number * spriteB.number
    elif spriteA.di and spriteB.di :
        spriteA.number = spriteA.number * spriteB.number

    elif spriteA.mu and ((spriteB.mu == False) and (spriteB.di == False)):
        spriteA.number = spriteA.number * spriteB.number
    elif spriteB.mu and ((spriteA.mu == False) and (spriteA.di == False)):
        spriteA.number = spriteA.number * spriteB.number

    elif spriteA.di and ((spriteB.mu == False) and (spriteB.di == False)):
        if spriteB.number%spriteA.number == 0:
            spriteA.number = int(spriteB.number/spriteA.number)
        else:
            if dokillA:
                spriteA.kill()
            if dokillB:
                spriteB.kill()
            return True
        
    elif spriteB.di and ((spriteA.mu == False) and (spriteA.di == False)):
        if spriteA.number%spriteB.number == 0:
            spriteA.number = int(spriteA.number/spriteB.number)
        else:
            if dokillA:
                spriteA.kill()
            if dokillB:
                spriteB.kill()
            return True
    else:
        if dokillA:
            spriteA.kill()
        if dokillB:
            spriteB.kill()
        return True
    if dokillB:
        spriteB.kill()
    spriteA.redraw()
    return False

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

        
        
        
    
    
