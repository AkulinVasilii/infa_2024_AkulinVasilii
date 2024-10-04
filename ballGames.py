import pygame
from pygame.draw import *
from random import randint
pygame.init()

sysfont = pygame.font.get_default_font()
print('system font :', sysfont)
font = pygame.font.SysFont(None, 48)

FPS = 1
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():
    '''рисует новый шарик '''
    
    global x, y, r
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click(event):
    print(x, y, r)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    
def click(event):
    print(x, y)

def compare(coords1, radius, coords2):
    return radius*radius >= (coords1[0] - coords2[0])*(coords1[0] - coords2[0]) + \
            (coords1[1] - coords2[1])*(coords1[1] - coords2[1])

pygame.display.update()
clock = pygame.time.Clock()
finished = False
events = []
score = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        #events.append(event)
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if compare(event.pos,r, (x,y)):
                score += 1
                img1 = font.render('score:' + str(score), True, BLUE)
                screen.blit(img1, (20, 50))
                
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

print(score)
pygame.quit()
