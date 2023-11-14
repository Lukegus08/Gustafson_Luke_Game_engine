# This File was created by Luke Gustafson on 10/24/23
# content from kids can code: http://kidscancode.org/blog/
#  colberated with table mates and exchanged diffent informantion between the group to try and figue out wat will be most effective
'''
GameDesign:

Goals - complete the level
Rules - dodge mobs, don't lose all hitpoints
have a three lives feture to compleate the level

FeatureGoals:

Have a coin feture that serves as a power up
Have new mobs generate off the screen and attack the player when on screen
add some kind of animation 


'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game: # the whole class for the game its self 
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.score = 5
        self.coins = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_JUMPPLATFORMS = pg.sprite.Group()
        self.all_Coins = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST: 
            # instantiation of the Platform class from setting.py 
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        
        # for j in JUMPPLATFORM_LIST:
        #     jump = JUMPPLATFORM(*j)
        #     self.all_sprites.add(jump)
        #     self.all_JUMPPLATFORMS.add(jump)

        for m in MOB_LIST: # the adding of the mob class from setting.py 
            mobs = Mob(*m)
            self.all_sprites.add(mobs)
            self.all_mobs.add(mobs)

        for c in COIN_LIST: # adding the coin class from setting.py 
            coin = Coin(*c)
            self.all_sprites.add(coin)
            self.all_Coins.add(coin)
        # for m in range(0,10):
        #     m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
        #     self.all_sprites.add(m)
        #     self.all_mobs.add(m)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            phits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if phits:
                self.player.pos.y = phits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = phits[0].speed*1.5
        # if self.player.vel.y >= 0:
        #     hits = pg.sprite.spritecollide(self.player, self.all_jumpPlatforms, False)
        #     if hits:
        #         self.player.pos.y = hits[0].rect.top
        #         self.player.vel.y = 2
        #         self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            mhits = pg.sprite.spritecollide(self.player, self.all_mobs, False)  # once the mob fetures are added and the results of the mob 
            if mhits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                self.score -= 1
                if self.player.rect.bottom >= mhits[0].rect.top - 1:
                    self.player.rect.top = mhits[0].rect.bottom
        elif self.player.vel.y <= 0:
            jhits = pg.sprite.spritecollide(self.player, self.all_jumpPlatforms, True) 
            if jhits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                if self.player.rect.bottom >= mhits[0].rect.top - 1:
                    self.player.rect.top = mhits[0].rect.bottom

        
                
        
        chits = pg.sprite.spritecollide(self.player, self.all_Coins, True) # add the coin feture to react to the game and once you interact to the game 
        if chits:
            print("i got a coin!")
            self.coins += 1
                
                


    def events(self):
        for event in pg.event.get():
        # check for closed window 
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10) # the display of the file for the score of the game 
        self.draw_text("Coins: " + str(self.coins), 22, WHITE, WIDTH/2, HEIGHT/20) # the siply of the coins
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y): # add the text to the game
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

G = Game()
while G.running:
    G.new()


pg.quit() # which closes the game 