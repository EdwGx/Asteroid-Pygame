import pygame
import random

from physic import*
from color import*
import MagBall
import Block
import menu
import end
import credit


class bullet_bar (object):
    def __init__(self):
        self.max = 8
        self.bullet = self.max
        self.reloading = False
        self.reloadTimer = 0

    def reinit(self):
        self.bullet = self.max
        self.reloading = False
        self.reloadTimer = 0

    def reload_bullet(self):
        if self.reloading == False:
            self.reloadTimer = pygame.time.get_ticks()
            self.reloading = True
        
    def draw(self,d_surface):
        x = 10
        y = 410
        self.reload_time = 2
        time_left = self.reload_time-(float(pygame.time.get_ticks())-float(self.reloadTimer))/1000

        if self.reloading:
            if time_left > 0:
                pygame.draw.rect(d_surface,
                         blue,
                         (x,y,int(150*time_left/self.reload_time),20))
                font = pygame.font.SysFont("Lucida Console",15,True)
                label = font.render(('RELOADING [%.1fs]'%(time_left)),True,white)
                d_surface.blit(label,(x+4,y+1))
            else:
                self.reloading = False
                self.bullet = self.max
                                    
        if self.reloading == False:
            for b_i in range(self.bullet):
                b_x = b_i*18 + x
                pygame.draw.polygon(d_surface,yellow,
                                    ((b_x,y+10),(b_x+8,y+10),(b_x+4,y)),0)

    def shoot(self):
        if self.bullet <= 0:
            self.reload_bullet()
            return False
        elif self.bullet == 1:
            self.bullet -= 1
            self.reload_bullet()
            return True
        else:
            self.bullet -= 1
            return True

class health_bar (object):
    def __init__(self):
        self.max = 100
        self.health = float(self.max)
        self.d_health = self.health
        self.losing = False
        self.lastHit = 0
        self.quick_check = False

    def reinit(self):
        self.health = float(self.max)
        self.d_health = self.health
        self.losing = False
        self.lastHit = 0
        self.quick_check = False
        
    def draw(self,d_surface):
        x = 10
        y = 440
        heal_time = 4000 #ms
        if self.losing:
            if self.health - self.d_health <= 0:
                self.losing = False
                self.d_health = self.health
                self.lastHit = pygame.time.get_ticks()
            else:
                self.d_health -= 4
        elif self.quick_check:
            if self.health < 96:
                self.health += 0.5
                self.d_health = self.health
            else:
                self.health = 100
                self.d_health = self.health
        elif (pygame.time.get_ticks() - self.lastHit) >= heal_time:
            self.quick_check = True        
        pygame.draw.rect(d_surface,red,(x,y,int(150*self.d_health/self.max),20))

    def hit(self,health_lose):
        self.quick_check = False
        if self.health - health_lose <= 0:
            return False
        else:
            self.health -= health_lose
            self.losing = True
            return True

class missile_controller(object):
    def __init__(self):
        self.call_timer = 18*60 #s*frame(60)
        self.current_timer = 0
        self.m_existed = False
    def reinit(self):
        self.call_timer = 18*60 #s*frame(60)
        self.current_timer = 0
    def draw(self,d_surface):
        if self.current_timer < self.call_timer:
            self.current_timer += 1
        elif self.current_timer < self.call_timer+140:
            global full_list
            if self.m_existed == False:
                missile = MagBall.Missile()
                missile.add(full_list,missile_list)
                self.m_existed = True
            point_list =((0,198),
                         (0,222),
                         (140,222),
                         (160,210),
                         (140,198))
            pygame.draw.polygon(d_surface,green,point_list,0)
            font = pygame.font.SysFont("Lucida Console",15,True)
            label = font.render('GUIDE MISSILE',True,white)
            d_surface.blit(label,(2,201))
            self.current_timer += 1
        else:
            self.current_timer = 0
            self.m_existed = False

            
            
            
        
                                        
def addBad():
    if getRandBool(65):
        bad = MagBall.Asteroid()
    else:
        bad = MagBall.Bomb()
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
                         pygame.Rect(10,sizeY-30,150*jumPower,20))
    else:
        jumPower = 0
        if moveY:
            moveY = False
            player.startFall()

def next_level():
    global player,spawn_speed
    spawn_speed += 2
    player.moveSpeed += 0.4

def init_game():
    global jumPower,bad_timer,block_timer,player_timer,move_dis
    global player,full_list,ball_list,bad_list,move_list,moveY,time_run
    global shoot_running,score,shoot_timer,bullet_bar,health_bar,spawn_speed
    jumPower = 1
    bad_timer = 0
    block_timer = 0
    player_timer = 0.0
    move_dis = 0.0
    score = 0
    shoot_timer = 0
    shoot_running = 0
    spawn_speed = 1
    player.kill()

    bullet_bar.reinit()
    health_bar.reinit()
    missile_controller.reinit()
    
    full_list.empty()
    ball_list.empty()
    bad_list.empty()
    move_list.empty()
    moveY = False
    player = MagBall.PlayerBall(200,-100)
    player.add(full_list)
    player.startFall()

        
                                    
pygame.init()
#Things must be do first
full_list = pygame.sprite.LayeredUpdates()
ball_list = pygame.sprite.Group()
bad_list = pygame.sprite.Group()
move_list = pygame.sprite.Group()
g_bullet = pygame.sprite.Group()
b_bullet = pygame.sprite.Group()
missile_list = pygame.sprite.Group() 

pygame.mouse.set_visible(True)
#Def varibles
sizeX = 800
sizeY = 500
jumPower = 1

bad_timer = 0
block_timer = 0
player_timer = 0.0
shoot_timer = 0
shoot_running = 0
spawn_speed = 1

move_dis = 0.0
score = 0 
scene = 1 #1:start menu 2:game 3:retry,win,quit 4:credit

background = pygame.image.load('background.jpg')
screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("My Game")

bullet_bar = bullet_bar()
health_bar = health_bar()
missile_controller = missile_controller()

#init player
player = MagBall.PlayerBall(200,-100)
player.add(full_list)
player.startFall()

moveY = False
done = False

 
clock = pygame.time.Clock()
 
while done == False:
    if scene == 1:
        return_number = menu.draw(screen)
        if return_number== 1:
            pygame.mouse.set_visible(False)
            scene = 2
        elif return_number == 2:
            scene = 4
            
            

        
    if scene == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    moveY = True
                    player.freeFall = False
    
                if event.key == pygame.K_e:
                    time_run = False
                if event.key == pygame.K_q:
                    next_level()
                if event.key == pygame.K_r:
                    bullet_bar.reload_bullet()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    moveY = False
                    player.startFall()
                if event.key == pygame.K_e:
                    time_run = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if bullet_bar.shoot():
                    bullet = MagBall.bullet(player.rect.centerx +40,player.rect.centery)
                    bullet.add(g_bullet,full_list)
                
            
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
        pygame.sprite.groupcollide(b_bullet,g_bullet,True,True)
        pygame.sprite.groupcollide(b_bullet,missile_list,True,True)
        coll_list = pygame.sprite.groupcollide(bad_list,missile_list,True,True)
        for bad in coll_list:
            if bad.good:
                score += 2
            else:
                score += 1
                pygame.mixer.music.load("expl.wav")
                pygame.mixer.music.play(1)

        coll_list = pygame.sprite.groupcollide(missile_list,move_list,True,True)
        score += (len(coll_list)*3)
                
        coll_list = pygame.sprite.spritecollide(player,bad_list,True)
        for bad in coll_list:
            if not(bad.good):
                alive = health_bar.hit(90)
                if not(alive):
                    player.losted = True
            else:
                alive = health_bar.hit(50)
                if not(alive):
                    player.losted = True

        coll_list = pygame.sprite.spritecollide(player,b_bullet,True)
        for bad in coll_list:
            alive = health_bar.hit(20)
            if not(alive):
                player.losted = True
                
                
                
        
        coll_list = pygame.sprite.groupcollide(bad_list,g_bullet,True,True)
        for bad in coll_list:
            if bad.good:
                score += 2

            else:
                score += 1
                pygame.mixer.music.load("expl.wav")
                pygame.mixer.music.play(1)
            

        coll_list = pygame.sprite.groupcollide(move_list,g_bullet,False,True)
        for bad in coll_list:
            bad.health -= 1
            bad.redraw()
            if bad.health <= 0:
                bad.kill()
                score += 3
                
                
        if pygame.time.get_ticks() - shoot_timer > 600 and shoot_running > 0:
            if shoot_block.alive():
                bullet = MagBall.bullet(shoot_block.rect.x -4,shoot_block.rect.y+48,False)
                bullet.add(b_bullet,full_list)
                bullet = MagBall.bullet(shoot_block.rect.x-4,shoot_block.rect.y+108,False)
                bullet.add(b_bullet,full_list)
                shoot_running -= 1
                shoot_timer = pygame.time.get_ticks()
            else:
                shoot_running = 0
                shoot_timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - shoot_timer > 3000:
            for b in move_list:
                if b.rect.x > 330 and b.rect.right < sizeX-10:
                    shoot_block = b
                    shoot_timer = pygame.time.get_ticks()
                    shoot_running = 4


        if block_timer <= move_dis:
            block = Block.Block()
            block.add(full_list,move_list)

            block_timer = move_dis + random.randint(10,14)*48 - spawn_speed
            if bad_timer <= 60:
                bad_timer = 60

        if bad_timer <= move_dis:
            addBad()
            bad_timer = move_dis + random.randint(2,5)*48 - spawn_speed
    
        move_list.update(player.moveSpeed)
        bad_list.update(player.moveSpeed,move_list)
        move_dis += player.moveSpeed

        player_timer += player.moveSpeed
        if player.losted:
            pygame.mixer.music.load("expl.wav")
            pygame.mixer.music.play(1)
            scene = 3
            pygame.mouse.set_visible(True)
        #draw
        screen.blit(background,background.get_rect())
    
        #real draw
        missile_controller.draw(screen)
        scoreLabel = font.render(('Score ') + str(score),True,white)
        screen.blit(scoreLabel,(10,10))
    
        player.update(move_list)
        g_bullet.update()
        b_bullet.update()
        missile_list.update()
        full_list.draw(screen)

        bullet_bar.draw(screen)
        health_bar.draw(screen)
        
        jump_bar()
        draw_mouse()
        #draw end
     
        pygame.display.flip()
        clock.tick(frames)


    if scene == 3:
        if end.draw(screen,score):
            pygame.mouse.set_visible(False)
            init_game()
            scene = 2
            
    if scene == 4:
        if credit.draw(screen):
            scene = 1
     

pygame.quit()

