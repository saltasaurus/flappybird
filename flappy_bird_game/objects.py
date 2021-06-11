import pygame as pg
import random
from .constants import BIRD_IMGS, PIPE_IMG, BASE_IMG

'''Flappy bird itself!'''
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
    
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        
        if d < 0:
            d -= 2

        self.y += d
        
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt >= -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # Nosedive animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        # Flapping wings animation
        elif self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]   
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0 

        rotated_image = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pg.mask.from_surface(self.img)

class Pipe:
    GAP = 300
    VEL = 5

    def __init__(self, x, score):
        self.x = x
        self.height = 0
        self.score = score

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        # Only keep one pipe at low scores
        self.TOP_BOT = random.randrange(0,2) # 0-> TOP | 1-> BOT
        # Diminishing single pipes
        self.SINGLE_PIPE = 1 if (random.randrange(5,16) - self.score > 0) else 0
 
        self.passed = False
        self.set_height()

    def set_height(self):
        self.__set_gap()
        rand_min = max(50, 130-self.GAP//10)
        rand_max = min(450, 270+self.GAP//10)
        self.height = random.randrange(rand_min, rand_max)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        print("Gap: ", self.bottom - self.top)

    def __set_gap(self):
        min_gap = 175

        x = 10*(self.score//4)
        if self.GAP - x > min_gap: 
            self.GAP -= x
        else:
            self.GAP = min_gap
        print("GAP = ", self.GAP)

    def move(self):
        self.x -= self.VEL 

    def draw(self, win):
        if self.score < 5 or self.SINGLE_PIPE:
            if self.TOP_BOT:    # Draw bottom pipe only
                win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
            else:               # Draw top pipe only
                win.blit(self.PIPE_TOP, (self.x, self.top))
        else:                   # Draw both pipes
            win.blit(self.PIPE_TOP, (self.x, self.top))
            win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def get_mask(self):
        return pg.mask.from_surface(self.PIPE_TOP), pg.mask.from_surface(self.PIPE_BOTTOM)

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask, bottom_mask = self.get_mask()
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # Collide with either pipe (only 1 exists)
        if self.score < 5 or self.SINGLE_PIPE:
            # BOT
            if self.TOP_BOT and b_point:
                return True
            # TOP
            elif not self.TOP_BOT and t_point:
                return True
        # Collide with either pipe (both exist)
        elif t_point or b_point:
            return True
        
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Game():

    def __init__(self):
        pass

    def run(self):
        pass

    def over(self):
        pass

    
