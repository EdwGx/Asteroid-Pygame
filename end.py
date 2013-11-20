#end.py
import pygame
from color import*

clock = pygame.time.Clock()
sizeX = 800
sizeY = 500
background = pygame.image.load('background.jpg')

def draw(screen,score):
    mouse_up = False
    rect1 =  pygame.Rect(0,0,100,60)
    rect1.center = (sizeX/2,sizeY/2 +50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_up = True
    mX = (pygame.mouse.get_pos())[0]
    mY = (pygame.mouse.get_pos())[1]
    screen.blit(background,background.get_rect())
    if rect1.collidepoint(mX,mY):
        if mouse_up:
            return True
        else:
            pygame.draw.rect(screen,darkgreen,rect1)
    else:
        pygame.draw.rect(screen,green,rect1)
    font = pygame.font.SysFont("comicsansms",30)
    Label = font.render('Retry',True,white)
    screen.blit(Label,
                ((sizeX - Label.get_width())/2,(sizeY - Label.get_height())/2 + 50))

    sfont = pygame.font.SysFont("comicsansms",50)
    scoreLabel = sfont.render(('Your Score is ') + str(score),True,white)
    screen.blit(scoreLabel,
                ((sizeX - scoreLabel.get_width())/2,(sizeY - scoreLabel.get_height())/2-50))
    
    pygame.display.flip()
    clock.tick(60)
    
        
