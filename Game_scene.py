import pygame
import random
from physic import*
from color import*
import MagBall

class game_scene(object):
    def __init__(self):
        self.sizeX = 800
        self.sizeY = 500
        self.jumPower = 1
        self.moveY = False
        self.mX = 0
        self.mY = 0
        self.full_list = pygame.sprite.LayeredUpdates()
        self.ball_list = pygame.sprite.LayeredUpdates()
        self.bad_list = pygame.sprite.Group()



    def addBad(self):
        bad = MagBall.BadBall()
        bad.add(self.full_list,self.ball_list,self.bad_list)
    
    def draw_mouse(self,surface):
        line_len = 10
        from_center = 5
        # - part
        pygame.draw.line(surface,red,
                         (self.mX-line_len-from_center,self.mY),
                         (self.mX-from_center,self.mY),3)
        pygame.draw.line(surface,red,
                         (self.mX+line_len+from_center,self.mY),
                         (self.mX+from_center,self.mY),3)
        # | part
        pygame.draw.line(surface,red,
                         (self.mX,self.mY-line_len-from_center),
                         (self.mX,self.mY-from_center),3)
        pygame.draw.line(surface,red,
                         (self.mX,self.mY+line_len+from_center),
                         (self.mX,self.mY+from_center),3)
        # center part
        pygame.draw.circle(surface,red,(self.mX,self.mY),3,0)

    def jump_bar(self,surface):
        if self.jumPower > 0:
            if self.jumPower > 0.3:
                draw_color = green
            else:
                draw_color = red
            pygame.draw.rect(surface,
                             draw_color,
                             pygame.Rect(10,self.sizeY-30,100*self.jumPower,20))
        else:
            self.jumPower = 0
            if self.moveY:
                self.moveY = False
                self.player.startFall()
    def run(self):
        pygame.init()
        

        pygame.mouse.set_visible(False)

        #Def varibles
        screen = pygame.display.set_mode([self.sizeX,self.sizeY])
        font = pygame.font.SysFont("comicsansms",30)
        pygame.display.set_caption("My Game")
        
        #init self.player
        self.player = MagBall.PlayerBall(1,200,400)
        self.player.add(self.full_list,self.ball_list)
        
        
        done = False
 
        clock = pygame.time.Clock()
 
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.moveY = True
                        self.player.freeFall = False
        
                    if event.key == pygame.K_e:
                        self.addBad()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.moveY = False
                        self.player.startFall()
        
            if self.moveY and self.jumPower > 0:
                if self.player.rect.y >= 2:
                    self.player.rect.y -= 2
                else:
                    self.player.rect.y = 0
            
                self.jumPower -= 0.02
            else:
                if self.jumPower <= 0.98:
                    self.jumPower += 0.02
            

            self.mX = (pygame.mouse.get_pos())[0]
            self.mY = (pygame.mouse.get_pos())[1]
            frames = 60
            #logic
            #coll_mouse_list = atom_list.get_sprites_at((self.mX,self.mX))
            for badBall in self.bad_list:
                for ballB in pygame.sprite.spritecollide(badBall,self.bad_list,False,pygame.sprite.collide_circle):
                    if not(badBall == ballB):
                        number_collide(badBall,ballB,True,True)
                    
        

            for badBall in pygame.sprite.spritecollide(self.player,self.bad_list,True,pygame.sprite.collide_circle):
                kill_player = number_collide(self.player,badBall,False,True)
                if kill_player:
                    self.player.losted = True
                    print ('you lost')

            #draw
            screen.fill(grey)
            #test
            t = pygame.time.get_ticks()
            timeLabel = font.render(str(t),True,green)
            screen.blit(timeLabel,(300,300))

            #real draw
            self.full_list.update()
            self.full_list.draw(screen)

            self.jump_bar(screen)
            self.draw_mouse(screen)
            #draw end
     
            pygame.display.flip()
            clock.tick(frames)
        pygame.quit()
