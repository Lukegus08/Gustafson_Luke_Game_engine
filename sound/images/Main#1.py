# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random

import os

vec = pg.math.Vector2

# setup asset folders here
game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, 'images')

# game settings
WIDTH = 360
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255) #color white
BLACK = (0, 0, 0) #color balck
RED = (255, 0, 0) #color red
GREEN = (0, 255, 0) #color green
BLUE = (0, 0, 255)#color blue
some_bytes = b'\xC3\xA9'
 
# Open in "wb" mode to
# write a new file, or 
# "ab" mode to append
with open("my_file.txt", "wb") as binary_file:
   
    # Write bytes to file
    binary_file.write(some_bytes) 
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50,50))
        # self.image.fill(GREEN)
        self.image = pg.image.load(os.path.join(img_folder, 'rock.gif')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        print(self.rect.center)
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s]:
            self.acc.y = 5
    def update(self):
        # self.rect.x += 5
        # self.rect.y += 5
        self.acc = vec(0,.98)
        self.controls()
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("i've collided...")
            if self.rect.bottom >= hits[0].rect.top-5:
                self.rect.bottom = hits[0].rect.top-5
                self.vel.y = 0
        print(all_platforms)
        # if friction - apply here
        self.acc.x += self.vel.x * -0.2
        self.acc.y += self.vel.y * -0.2
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y > HEIGHT:
            self.rect.y = 0
        self.rect.midbottom = self.pos

# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        # self.image = pg.image.load(os.path.join(img_folder, 'rock.gif')).convert()
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.pos = vec(WIDTH/2, HEIGHT/2)
        # self.vel = vec(0,0)
        # self.acc = vec(0,0)
        print(self.rect.center)


# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My game...")
clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()

# instantiate the classes
player = Player()
plat = Platform(150, 300, 100, 30)
plat1 = Platform(200, 200, 100, 30)

# add instances to groups
all_sprites.add(player)
all_sprites.add(plat)
all_sprites.add(plat1)
all_platforms.add(plat)
all_platforms.add(plat1)

# Game loop
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False

    ###############Update###################
    # update all sprites
    all_sprites.update()
    
    ###############Draw#####################
    # draw the background screen
    screen.fill(BLACK)
    # draw all sprites 
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()