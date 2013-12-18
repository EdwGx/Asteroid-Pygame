import pygame
import random

from physic import*
from color import*
import MagBall
import Block
import menu
import end
import credit
import mode

class jump_bar(object):
    def __init__(self,x=10,y=470):
        self.x = x
        self.y = y
        self.jumPower = float(1)
        self.moving = False
        self.spend = 0.02

    def reinit(self):
        self.jumPower = float(1)
        self.moving = False
        self.spend = 0.02

    def start_move(self):
        self.moving = True

    def stop_move(self,p_sp):
        self.moving = False
        p_sp.startFall()
        
    def draw(self,screen,p_sp):
        if self.moving and self.jumPower > 0:
            if p_sp.rect.y >= 2:
                p_sp.rect.y -= 2
            else:
                p_sp.rect.y = 0
            self.jumPower -= self.spend
        elif self.jumPower <= 0.98:
                self.jumPower += 0.02

        if self.jumPower > 0:
            if self.jumPower > 0.3:
                draw_color = darkgreen
            else:
                draw_color = red
            pygame.draw.rect(screen,draw_color,pygame.Rect(self.x,self.y,150*self.jumPower,20))
        else:
            self.jumPower = 0
            if self.moving:
                self.moving = False
            p_sp.startFall()

class bullet_bar (object):
    def __init__(self,x=10,y=410):
        self.x = x
        self.y = y
        self.max = 8
        self.bullet = self.max
        self.reloading = False
        self.reloadTimer = 0
        self.reload_time = 2

    def reinit(self):
        self.max = 8
        self.bullet = self.max
        self.reloading = False
        self.reloadTimer = 0
        self.reload_time = 2

    def reload_bullet(self):
        if self.reloading == False:
            self.reloadTimer = pygame.time.get_ticks()
            self.reloading = True
        
    def draw(self,d_surface):
        
        time_left = self.reload_time-(float(pygame.time.get_ticks())-float(self.reloadTimer))/1000

        if self.reloading:
            if time_left > 0:
                pygame.draw.rect(d_surface,
                         blue,
                         (self.x,self.y,int(150*time_left/self.reload_time),20))
                font = pygame.font.SysFont("Lucida Console",15,True)
                label = font.render(('RELOADING [%.1fs]'%(time_left)),True,white)
                d_surface.blit(label,(self.x+4,self.y+1))
            else:
                self.reloading = False
                self.bullet = self.max
                                    
        if self.reloading == False:
            for b_i in range(self.bullet):
                b_x = b_i*18 + self.x
                pygame.draw.polygon(d_surface,yellow,
                                    ((b_x,self.y+10),(b_x+8,self.y+10),(b_x+4,self.y)),0)

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
    def __init__(self,x=10,y=440):
        self.x = x
        self.y = y
        self.max = 100
        self.health = float(self.max)
        self.d_health = self.health
        self.losing = False
        self.lastHit = 0
        self.quick_check = False
        self.heal = 0.1
        self.heal_time = 3000

    def reinit(self):
        self.health = float(self.max)
        self.d_health = self.health
        self.losing = False
        self.lastHit = 0
        self.quick_check = False
        self.heal = 0.1
        self.heal_time = 3000
        
    def draw(self,d_surface):
        if self.losing:
            if self.health - self.d_health <= 0:
                self.losing = False
                self.d_health = self.health
                self.lastHit = pygame.time.get_ticks()
            else:
                self.d_health -= 4
        elif self.quick_check:
            if self.health < 100:
                self.health += self.heal
                self.d_health = self.health
            else:
                self.health = 100
                self.d_health = self.health
        elif (pygame.time.get_ticks() - self.lastHit) >= self.heal_time:
            self.quick_check = True        
        pygame.draw.rect(d_surface,red,(self.x,self.y,int(150*self.d_health/self.max),20))
        font = pygame.font.SysFont("Lucida Console",15,True)
        label = font.render(str(int(self.health)),True,white)
        d_surface.blit(label,(self.x+1,self.y+1))

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
        self.m_existed = False
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


def next_level():
    global spawn_speed
    spawn_speed += 0.04

def init_game():
    global jumPower,bad_timer,block_timer,player_timer,move_dis
    global full_list,ball_list,bad_list,move_list,moveY,time_run
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
            
    full_list.empty()
    ball_list.empty()
    bad_list.empty()
    move_list.empty()
    moveY = False

def reinit_player(number):
    global player,player1,player2,player1_move,player2_move,jump_bar1,jump_bar2,bullet_bar1,bullet_bar2,health_bar1,health_bar2,missile_controller
    if number == 1:
        jump_bar1.reinit()
        bullet_bar1.reinit()
        health_bar1.reinit()
        missile_controller.reinit()
        
        player = MagBall.PlayerBall(200,-100)
        player.add(full_list)
        player.startFall()
        
    elif number == 2:
        jump_bar1.reinit()
        jump_bar2.reinit()
        bullet_bar1.reinit()
        bullet_bar2.reinit()
        health_bar1.reinit()
        health_bar2.reinit()
        
        player1 = MagBall.PlayerBall(170,200)
        player1.add(full_list)
        player2 = MagBall.PlayerBall(230,400,True)
        player2.add(full_list)
        player1_move = 0
        player2_move = 0

def init_player(number):
    global player,jump_bar1,jump_bar2,player1,player2,player1_move,player2_move,bullet_bar1,bullet_bar2,health_bar1,health_bar2,missile_controller
    if number == 1:
        bullet_bar1 = bullet_bar(10)
        health_bar1 = health_bar(10)
        jump_bar1 = jump_bar(10)
        missile_controller = missile_controller()
        
        player = MagBall.PlayerBall(200,-100)
        player.add(full_list)
        player.startFall()
        
    elif number == 2:
        bullet_bar1 = bullet_bar(10)
        bullet_bar2 = bullet_bar(640)
        health_bar1 = health_bar(10)
        health_bar2 = health_bar(640)
        jump_bar1 = jump_bar(10)
        jump_bar2 = jump_bar(640)
        
        player1 = MagBall.PlayerBall(170,200)
        player1.add(full_list)
        player2 = MagBall.PlayerBall(230,400,True)
        player2.add(full_list)
        player1_move = 0
        player2_move = 0

        
                                    
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
scene = 1 #1:start menu 2:game 3:retry,win,quit 4:credit 5:2-Player 6:2-Player retry
#7:mode menu

background = pygame.image.load('background.jpg')
icon = pygame.image.load('icon@2x.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode([sizeX,sizeY])
font = pygame.font.SysFont("comicsansms",30)
pygame.display.set_caption("Asteroid")


moveY = False
done = False
is_init_1 = True
is_init_2 = True
 
clock = pygame.time.Clock()
 
while done == False:
    if scene == 1:
        return_number = menu.draw(screen)
        if return_number== 1:
            init_game()
            if is_init_1:
                init_player(1)
                is_init_1 = False
            else:
                reinit_player(1)
            scene = 7
        elif return_number== 2:
            pygame.mouse.set_visible(False)
            init_game()
            if is_init_2:
                init_player(2)
                is_init_2 = False
            else:
                reinit_player(2)
            scene = 5
        elif return_number == 3:
            scene = 4
            
    if scene == 7:
        return_number = mode.draw(screen)
        if return_number == 2:
            bullet_bar1.max = 6
            bullet_bar1.bullet = 6
            scene = 2
            pygame.mouse.set_visible(False)
        elif return_number == 1:
            bullet_bar1.max = 8
            bullet_bar1.bullet = 8
            bullet_bar1.reload_time = 1
            missile_controller.call_timer = 6*60
            jump_bar1.spend = 0.006
            health_bar1.heal = 0.3
            health_bar1.heal_time = 500
            scene = 2
            pygame.mouse.set_visible(False)
        
            
        

        
    if scene == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_bar1.start_move()
                    player.freeFall = False
    
                if event.key == pygame.K_e:
                    time_run = False
                if event.key == pygame.K_r:
                    bullet_bar1.reload_bullet()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    jump_bar1.stop_move(player)
                if event.key == pygame.K_e:
                    time_run = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if bullet_bar1.shoot():
                    bullet = MagBall.bullet(player.rect.centerx +40,player.rect.centery)
                    bullet.add(g_bullet,full_list)
        if done:
            break

    
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
                alive = health_bar1.hit(90)
                if not(alive):
                    player.losted = True
            else:
                alive = health_bar1.hit(50)
                if not(alive):
                    player.losted = True

        coll_list = pygame.sprite.spritecollide(player,b_bullet,True)
        for bad in coll_list:
            alive = health_bar1.hit(20)
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
                bullet = MagBall.bullet(shoot_block.rect.x -4,shoot_block.rect.y+10,False)
                bullet.add(b_bullet,full_list)
                bullet = MagBall.bullet(shoot_block.rect.x-4,shoot_block.rect.y+146,False)
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

        spawn_speed += 0.04
        if block_timer <= move_dis:
            block = Block.Block()
            block.add(full_list,move_list)
            
            block_timer = move_dis + random.randint(10,14)*48 - spawn_speed
            if block_timer < 10:
                bad_timer = 10

        if bad_timer <= move_dis:
            addBad()
            bad_timer = move_dis + random.randint(2,5)*48 - spawn_speed
            if bad_timer <= 10:
                bad_timer = 10
    
        move_list.update(player.moveSpeed)
        bad_list.update(player.moveSpeed)
        move_dis += player.moveSpeed

        player_timer += player.moveSpeed
        if player.losted:
            pygame.mixer.music.load("lose.wav")
            pygame.mixer.music.play(1)
            scene = 3
            pygame.mouse.set_visible(True)
        #draw
        screen.blit(background,background.get_rect())
    
        #real draw
        missile_controller.draw(screen)
        scoreLabel = font.render(('Score ') + str(score),True,white)
        screen.blit(scoreLabel,(10,10))
    
        player.update()
        g_bullet.update()
        b_bullet.update()
        missile_list.update()
        full_list.draw(screen)

        bullet_bar1.draw(screen)
        health_bar1.draw(screen)
        jump_bar1.draw(screen,player)
        draw_mouse()
        #draw end
     
        pygame.display.flip()
        clock.tick(frames)

    if scene == 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    jump_bar1.start_move()
                    player1.freeFall = False
                if event.key == pygame.K_UP:
                    jump_bar2.start_move()
                    player2.freeFall = False
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    if bullet_bar1.shoot()  and not(player1.losted):
                        bullet = MagBall.bullet(player1.rect.centerx +40,player1.rect.centery)
                        bullet.shooter = 1
                        bullet.add(g_bullet,full_list)
                if event.key == pygame.K_RIGHT:
                    if bullet_bar2.shoot() and not(player2.losted):
                        bullet = MagBall.bullet(player2.rect.centerx +40,player2.rect.centery)
                        bullet.shooter = 2
                        bullet.add(g_bullet,full_list)
                if event.key == pygame.K_w:
                    jump_bar1.stop_move(player1)
                if event.key == pygame.K_UP:
                    jump_bar2.stop_move(player2)
        if done:
            break
            
                    
        mX = (pygame.mouse.get_pos())[0]
        mY = (pygame.mouse.get_pos())[1]
    
        
    
        frames = 60
        #logic
        pygame.sprite.groupcollide(b_bullet,g_bullet,True,True)

        if not(player1.losted):
            coll_list = pygame.sprite.spritecollide(player1,bad_list,True)
            for bad in coll_list:
                if not(bad.good):
                    alive = health_bar1.hit(90)
                    if not(alive):
                        player1.kill()
                        player1.losted = True
                else:
                    alive = health_bar1.hit(50)
                    if not(alive):
                        player1.kill()
                        player1.losted = True
    
            coll_list = pygame.sprite.spritecollide(player1,b_bullet,True)
            for bad in coll_list:
                alive = health_bar1.hit(20)
                if not(alive):
                    player1.kill()
                    player1.losted = True
                
        if not(player2.losted):
            coll_list = pygame.sprite.spritecollide(player2,bad_list,True)
            for bad in coll_list:
                if not(bad.good):
                    alive = health_bar2.hit(90)
                    if not(alive):
                        player2.kill()
                        player2.losted = True
                else:
                    alive = health_bar2.hit(50)
                    if not(alive):
                        player2.kill()
                        player2.losted = True

            coll_list = pygame.sprite.spritecollide(player2,b_bullet,True)
            for bad in coll_list:
                alive = health_bar2.hit(20)
                if not(alive):
                    player2.kill()
                    player2.losted = True
                
                
        for bad in bad_list:
            coll_list = pygame.sprite.spritecollide(bad,g_bullet,True)
            if len(coll_list) > 0:
                bad.kill()
                hit_b = coll_list[0]
                if hit_b.shooter == 1:
                    if bad.good:
                        player1.score += 2
                    else:
                        player1.score += 1
                        pygame.mixer.music.load("expl.wav")
                        pygame.mixer.music.play(1)
                elif hit_b.shooter == 2:
                    if bad.good:
                        player2.score += 2
                    else:
                        player2.score += 1
                        pygame.mixer.music.load("expl.wav")
                        pygame.mixer.music.play(1)
            
        for bad in move_list:
            coll_list = pygame.sprite.spritecollide(bad,g_bullet,True)
            if len(coll_list) > 0:
                for bu in coll_list:
                    bad.health -= 1
                    bad.redraw()
                    if bad.health <= 0:
                        bad.kill()
                        if bu.shooter == 1:
                            player1.score += 3
                        elif bu.shooter == 2:
                            player2.score += 3
                
                
        if pygame.time.get_ticks() - shoot_timer > 600 and shoot_running > 0:
            if shoot_block.alive():
                bullet = MagBall.bullet(shoot_block.rect.x -4,shoot_block.rect.y+10,False)
                bullet.add(b_bullet,full_list)
                bullet = MagBall.bullet(shoot_block.rect.x-4,shoot_block.rect.y+146,False)
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

        spawn_speed += 0.04
        if block_timer <= move_dis:
            block = Block.Block()
            block.add(full_list,move_list)
            block_timer = move_dis + random.randint(10,14)*48 - spawn_speed
            if block_timer < 10:
                block_timer = 10

        if bad_timer <= move_dis:
            addBad()
            bad_timer = move_dis + random.randint(2,5)*48 - spawn_speed
            if bad_timer < 10:
                bad_timer = 10
    
        move_list.update(0.8)
        bad_list.update(0.8)
        move_dis += 0.8

        if not(player1_move == 0):
            if (player1_move == 1) and (player1.rect.bottom < 496):
                player1.rect.y += 4
            elif (player1_move == 2) and (player1.rect.top > 6):
                player1.rect.y -= 4
                
        '''if not(player2_move == 0):
            if (player2_move == 1) and (player2.rect.bottom < 496):
                player2.rect.y += 4
            elif (player2_move == 2) and (player2.rect.top > 6):
                player2.rect.y -= 4'''

        if player1.losted and player2.losted:
            pygame.mixer.music.load("lose.wav")
            pygame.mixer.music.play(1)
            scene = 6
            pygame.mouse.set_visible(True)
        #draw
        screen.blit(background,background.get_rect())
        
        
        #real draw
        scoreLabel = font.render(('Score ') + str(player1.score),True,white)
        screen.blit(scoreLabel,(10,10))
        
        scoreLabel2 = font.render(('Score ') + str(player2.score),True,white)
        screen.blit(scoreLabel2,(800-scoreLabel2.get_width()-10,10))
        player1.update()
        player2.update()
    
        g_bullet.update()
        b_bullet.update()
        full_list.draw(screen)
        if not(player1.losted): 
            bullet_bar1.draw(screen)
            health_bar1.draw(screen)
            jump_bar1.draw(screen,player1)

        if not(player2.losted): 
            bullet_bar2.draw(screen)
            health_bar2.draw(screen)
            jump_bar2.draw(screen,player2)
            
        
        
        #draw end
     
        pygame.display.flip()
        clock.tick(frames)



    if scene == 3:
        event_b = end.draw(screen,score)
        if event_b == 1:
            pygame.mouse.set_visible(False)
            init_game()
            reinit_player(1)
            scene = 7
        elif event_b == 2:
            scene = 1
            
            
    if scene == 4:
        if credit.draw(screen):
            scene = 1

    if scene == 6:
        event_b = end.draw(screen,player1.score,True,player2.score)
        if event_b == 1:
            pygame.mouse.set_visible(False)
            init_game()
            reinit_player(2)
            scene = 5
        elif event_b == 2:
            scene = 1
     

pygame.quit()

