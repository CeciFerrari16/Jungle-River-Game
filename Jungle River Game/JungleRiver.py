# Player moves, enemies start
import pygame
import random
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60 

# set up assets
"""
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")"""
img_dir = path.join(path.dirname(__file__), "img")

# Colour used
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CELESTE = (0, 196, 255)

# start pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle River")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("CHILLER")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (41, 127))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

# enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img1, (33, 92))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.rect.x = random.randrange(WIDTH - self.rect.width)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 15:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)

class Mob1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img2, (33, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.speedx = random.randrange(-3,3)
       

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
# game screen 
def title_screen():
    screen.blit(title, title_rect)
    draw_text(screen, "Benvenuto in" , 18, WIDTH / 2, 10)
    draw_text(screen, "JUNGLE RIVER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Usa le frecce per muoverti e schiva i tronchi!", 25, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Premi un tasto per iniziare", 20, WIDTH / 2, HEIGHT * 5 / 8)
    pygame.display.flip()
    waiting = True 
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "GAME OVER", 66, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Premi Spazio per ricominciare", 22, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True 
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            else:
                waiting = True
                

# load all graphics
title = pygame.image.load(path.join(img_dir, "JungleVine2.png")).convert()
title_rect = title.get_rect()
background = pygame.image.load(path.join(img_dir,"waterground.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "boat.png")).convert()
# mob 
mob_img1 = pygame.image.load(path.join(img_dir,"medium1.png" )).convert()
mob_img2 = pygame.image.load(path.join(img_dir,"short1.png" )).convert()

# Game loop
game_over = True
running = True
while running:
    if game_over:
        title_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(3):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        for i in range(5):
            m1 = Mob1()
            all_sprites.add(m1)
            mobs.add(m1)

    # keep running at right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get(): 
        # check closing the window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        game_over = True
        show_go_screen()
    
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # after draw, flip the display
    pygame.display.flip()

pygame.quit()