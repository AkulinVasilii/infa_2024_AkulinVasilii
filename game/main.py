from os import path

img_dir = path.join(path.dirname(__file__), 'graphics_forgame')

import pygame
import random

WIDTH = 600
HEIGHT = 750
FPS = 90

# Imagine the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Create window and game and base classes
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# loading background
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
# loading graphics for player, fighter and bullets sprite
player_img = pygame.image.load(path.join(img_dir, "x-wing.png")).convert()
fighter_img = pygame.image.load(path.join(img_dir, "fighter of Empire.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserGreen.png")).convert()

# sprite of player
class Player(pygame.sprite.Sprite):
    # initialisation
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
    # drawing per iteration
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    # method for shooting        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
            
            
# sprite of the comets and fighters
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = fighter_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(fighter_img, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# create class for observing the laser gun's hits
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(bullet_img, (5, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # delete whether it out of screen
        if self.rect.bottom < 0:
            self.kill()
            
# install a timer
clock = pygame.time.Clock()
# create groups of sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
bullets = pygame.sprite.Group()


# Main loop of game
running = True
while running:
    # keeping loop on correct speed
    clock.tick(FPS)
    
    # input of process(event)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # check the player's movement    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -8
            if event.key == pygame.K_RIGHT:
                player.speedx = 8
        # check the player's shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update all of the objects
    all_sprites.update()
    # checking if player faces with something
    hits_npc = pygame.sprite.spritecollide(player, mobs, False)
    if hits_npc:
        running = False
    # check if player gets to comet or fighter
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    # Rendering screen
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # flipping screen after drawing
    pygame.display.flip()

pygame.quit()