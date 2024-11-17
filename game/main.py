from os import path
# available path to directory
img_dir = path.join(path.dirname(__file__), 'graphics_forgame')
snd_dir = path.join(path.dirname(__file__), 'sound_game')
import pygame
import random
import shelve

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

#create class for saving information about players and record score
class Save:
    def __init__(self):
        self.file = shelve.open('data')
        self.file['name'] = ''
        
    def add(self, name, value):
        self.file[name] = value
    
    def get(self, name):
        return self.file[name]
    
    def _del_(self):
        self.file.close()

save_data = Save()

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
an_shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'enemy_lr.wav'))
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
enemybullet_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()

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
            
    # method for player's shooting        
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
        self.cd_shoot = 0
        self.enemy_bullets = []
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
    # function for mob's shooting in deed don't work properly       
    def shoot(self):
        if not self.cd_shoot:
            an_shoot_sound.play() 
            new_bullet = enemybullet(self.rect.x, self.rect.y+15)
            new_bullet.find_path(random.randrange(10, 600), random.randrange(self.rect.y, 750))
            self.enemy_bullets.append(new_bullet)
            all_sprites.add(new_bullet)
            enemybullets.add(new_bullet)
            self.cd_shoot = 200
        else:
            self.cd_shoot -= 1   
            

#showing start screen            
def show_go_screen():
    save_data.add('name', 'Guest')
    need_input = False
    input_text = '' 
    waiting = True
    while waiting:
        clock.tick(FPS)
        # starting menu with opportunity to create a profile
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    waiting = False
            if need_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    need_input = False
                    save_data.add('name', input_text)
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text)<10:
                        input_text += event.unicode           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            need_input = True 
        # drawing start screen    
        screen.blit(background, background_rect)
        draw_text(screen, "STAR WARS", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Press RSHIFT to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(screen, input_text, 32, WIDTH/2, HEIGHT/2)
        pygame.display.flip()
            
# class for enemy's bullets in deed don't work
class enemybullet(pygame.sprite.Sprite):
    # class initialisation
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemybullet_img
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(enemybullet_img, (5, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.x = x
        self.y = y
        self.speedx = 8
        self.speedy = 0
        self.dest_x = random.randrange(10, 600)
        self.dest_y = random.randrange(y, 750)
    # bullet control
    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        # delete whether it out of screen
        if self.x < 0 or self.x > 600:
            self.kill()            
        if self.y > 750 or self.y < 0:
            self.kill()
            
    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y
        delta_x = dest_x - self.x
        if delta_x == 0:
            self.speedy = 10
            self.speedx = 0
        elif delta_x < 0:
            self.speedx = -8
            count_x = abs(delta_x)//self.speedx
            delta_y = dest_y - self.y
            self.speedy = delta_y // count_x
        else:
            self.speedx = 8
            count_x = abs(delta_x)//self.speedx
            delta_y = dest_y - self.y
            self.speedy = delta_y // count_x
        
# create class for observing the player's laser gun's hits
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
enemybullets = pygame.sprite.Group()
score = 0
max_cur_score = 0
max_score = save_data.get('max_score')
print(max_score)
pygame.mixer.music.play(loops=-1)

# Main loop of game
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
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
        # checking if player beats the record score
        if max_score < score:
            max_score = score
            save_data.add('best_player_name', save_data.get('name'))
            save_data.add('max_score', max_score)
            
        
        game_over = True
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
    draw_text(screen, "Score of current game: " + str(score), 20, 1*WIDTH / 4, 40)
    draw_text(screen, "Max score: " + str(max_score), 20, 3 * WIDTH / 4, 40)
    draw_text(screen, "Name of current player: " + save_data.get('name'), 20, 1 * WIDTH / 4, 10)
    draw_text(screen, "Name of best player: " + save_data.get('best_player_name'), 20, 3 * WIDTH / 4, 10)
    # flipping screen after drawing
    pygame.display.flip()

pygame.quit()