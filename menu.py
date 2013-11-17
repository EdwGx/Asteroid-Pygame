#menu.py
import pygame
from color import*

clock = pygame.time.Clock()
sizeX = 800
sizeY = 500

def draw(screen):
    mouse_up = False
    rect1 =  pygame.Rect(0,0,300,150)
    rect1.center = (sizeX/2,sizeY/2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]
    screen.fill(grey)
    if rect1.collidepoint(mX,mY):
        if mouse_up:
            return True
        else:
            pygame.draw.rect(screen,darkgreen,rect1)
    else:
        pygame.draw.rect(screen,green,rect1)
    font = pygame.font.SysFont("comicsansms",30)
    Label = font.render('Start',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2))
    pygame.display.flip()
    clock.tick(60)
    
        
