import pygame
import random

from physic import*
from color import*
import MagBall
import Block
import menu
import end

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
            draw_color = darkgreen
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

def init_game():
    global jumPower,bad_timer,block_timer,player_timer,move_dis
    global player,full_list,ball_list,bad_list,move_list,moveY
    jumPower = 1
    bad_timer = 0
    block_timer = 0
    player_timer = 0.0
    move_dis = 0.0
    player.kill()
    full_list.empty()
    ball_list.empty()
    bad_list.empty()
    move_list.empty()
    moveY = False
    player = MagBall.PlayerBall(1,200,-100)
    player.add(full_list,ball_list)
    

    
                                     
pygame.init()
#Things must be do first
full_list = pygame.sprite.LayeredUpdates()
ball_list = pygame.sprite.LayeredUpdates()
bad_list = pygame.sprite.Group()
move_list = pygame.sprite.Group()

pygame.mouse.set_visible(True)

#Def varibles
sizeX = 800
sizeY = 500
jumPower = 1
bad_timer = 0
block_timer = 0
player_timer = 0.0
move_dis = 0.0
scene = 1 #1:start menu 2:game 3:retry,win,quit

screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("My Game")

#init player
player = MagBall.PlayerBall(1,200,-100)
player.add(full_list,ball_list)
player.startFall()


moveY = False
done = False

 
clock = pygame.time.Clock()
 
while done == False:
    if scene == 1:
        if menu.draw(screen):
            pygame.mouse.set_visible(False)
            scene = 2
            

        
    if scene == 2:
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


        if block_timer <= move_dis:
            block = Block.Block()
            block.add(full_list,move_list)
            block_timer = move_dis + random.randint(10,14)*48
            if bad_timer <= 60:
                bad_timer = 60

        if bad_timer <= move_dis:
            addBad()
            bad_timer = move_dis + random.randint(2,5)*48
    
        move_list.update(player.moveSpeed)
        bad_list.update(player.moveSpeed,move_list)
        move_dis += player.moveSpeed
        player_timer += player.moveSpeed
        if player.losted:
            scene = 3
            pygame.mouse.set_visible(True)
        #draw
        screen.fill(grey)
    
        #real draw
        scoreLabel = font.render(('Score '+str(player.number)),True,white)
        screen.blit(scoreLabel,(10,10))

        distanceLabel = font.render((str(int(player_timer/3600*100))+'%'),True,white)
        screen.blit(distanceLabel,(sizeX - 10 - distanceLabel.get_width(),10))
    
    
        
        
        player.update(move_list)
        full_list.draw(screen)

        jump_bar()
        #draw_mouse()
        #draw end
     
        pygame.display.flip()
        clock.tick(frames)

    if scene == 3:
        if end.draw(screen):
            pygame.mouse.set_visible(False)
            init_game()
            scene = 2
     

pygame.quit()

