from os import path
# available path to directory
img_dir = path.join(path.dirname(__file__), 'graphics_forgame')
snd_dir = path.join(path.dirname(__file__), 'sound_game')
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

# function for adding text
font_name = pygame.font.match_font('StarJedi Special Edition')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Start the game and creation of a screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# loading sound effects
# sound of shoot
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_gun.wav'))
# sounds of explosions
expl_sounds = []
for snd in ['space_expl1.wav', 'space_expl2.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
# movement sound effects
move_sounds = []
for move in ['manevr1.wav', 'manevr2.wav']:
    move_sounds.append(pygame.mixer.Sound(path.join(snd_dir, move)))
#loading music
pygame.mixer.music.load(path.join(snd_dir, 'music.mp3'))
pygame.mixer.music.set_volume(1)

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
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        shoot_sound.play()
            
            
# sprite of the comets and fighters
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = fighter_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(fighter_img, (35, 35))
        self.rect = self.image.get_rect()
        self.radius = 15
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
    # class initialisation
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(bullet_img, (5, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    # bullet control
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
score = 0
pygame.mixer.music.play(loops=-1)

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
                move_sounds[0].play()
            if event.key == pygame.K_RIGHT:
                player.speedx = 8
                move_sounds[1].play()
        # check the player's shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update all of the objects
    all_sprites.update()
    # checking if player faces with something
    hits_npc = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits_npc:
        running = False
    # check if player gets to fighter
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        expl_sounds[0].play()
        all_sprites.add(m)
        mobs.add(m)
    # Rendering screen
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # flipping screen after drawing
    pygame.display.flip()

pygame.quit()