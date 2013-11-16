import pygame
import random

from physic import*
from color import*
import MagBall
import Block

def addBad():
    bad = MagBall.BadBall()
    bad.add(full_list,ball_list,bad_list)
    
def draw_mouse():
    global mX,mY
    line_len = 10
    from_center = 5
    # - part
    pygame.draw.line(screen,red,
                     (mX-line_len-from_center,mY),
                     (mX-from_center,mY),3)
    pygame.draw.line(screen,red,
                     (mX+line_len+from_center,mY),
                     (mX+from_center,mY),3)
    # | part
    pygame.draw.line(screen,red,
                     (mX,mY-line_len-from_center),
                     (mX,mY-from_center),3)
    pygame.draw.line(screen,red,
                     (mX,mY+line_len+from_center),
                     (mX,mY+from_center),3)
    # center part
    pygame.draw.circle(screen,red,(mX,mY),3,0)

def jump_bar():
    global jumPower, moveY
    if jumPower > 0:
        if jumPower > 0.3:
            draw_color = green
        else:
            draw_color = red
        pygame.draw.rect(screen,
                         draw_color,
                         pygame.Rect(10,sizeY-30,100*jumPower,20))
    else:
        jumPower = 0
        if moveY:
            moveY = False
            player.startFall()

    
                                     
pygame.init()
#Things must be do first
full_list = pygame.sprite.LayeredUpdates()
ball_list = pygame.sprite.LayeredUpdates()
bad_list = pygame.sprite.Group()
move_list = pygame.sprite.Group()

pygame.mouse.set_visible(False)

#Def varibles
sizeX = 800
sizeY = 500
jumPower = 1
bad_timer = 0
block_timer = 0
move_dis = 0.0

screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("My Game")

#init player
player = MagBall.PlayerBall(1,200,400)
player.add(full_list,ball_list)


moveY = False
done = False

 
clock = pygame.time.Clock()
 
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moveY = True
                player.freeFall = False

            if event.key == pygame.K_e:
                addBad()
            if event.key == pygame.K_q:
                block = Block.Block()
                block.add(full_list,move_list)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                moveY = False
                player.startFall()
        
    if moveY and jumPower > 0:
        if player.rect.y >= 2:
            player.rect.y -= 2
        else:
            player.rect.y = 0
            
        jumPower -= 0.02
    else:
        if jumPower <= 0.98:
            jumPower += 0.02
            

    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]

    
    
    frames = 60
    #logic
    #coll_mouse_list = atom_list.get_sprites_at((mX,mY))
    for badBall in bad_list:
        for ballB in pygame.sprite.spritecollide(badBall,bad_list,False,pygame.sprite.collide_circle):
            if not(badBall == ballB):
                number_collide(badBall,ballB,True,True)
            
        

    for badBall in pygame.sprite.spritecollide(player,bad_list,True,pygame.sprite.collide_circle):
        kill_player = number_collide(player,badBall,False,True)
        if kill_player:
            player.losted = True
            print ('you lost')

    

    if block_timer <= move_dis:
        block = Block.Block()
        block.add(full_list,move_list)
        block_timer = move_dis + random.randint(10,14)*48
        if bad_timer <= 60:
            bad_timer = 60

    if bad_timer <= move_dis:
        addBad()
        bad_timer = move_dis + random.randint(2,5)*48

    if player.rect.y == (sizeY - player.radius*2):
        move_list.update(0)
        bad_list.update(0,move_list)
    else:
        move_list.update(0.8)
        bad_list.update(0.8,move_list)
        move_dis += 0.8
    #draw
    screen.fill(grey)
    
    #real draw

        
        
    player.update()
    full_list.draw(screen)

    jump_bar()
    #draw_mouse()
    #draw end
     
     pygame.display.flip()
    clock.tick(frames)
     

pygame.quit()

