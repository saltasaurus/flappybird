import pygame as pg 
import time
import json

#from pygame.constants import MOUSEBUTTONDOWN

from .objects import Bird, Pipe, Base
from .constants import *

def draw_window(win, bird, pipes, base, score, run):
    '''Update game graphics'''
    win.blit(BG_IMG, (0,0))

    # Draw objects: Pipes, base & flappy bird
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    bird.draw(win)

    # Game running
    if run:
        # Display score on screen
        text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Game over
    else:
        text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH//2 - text.get_width()//2, WIN_HEIGHT//2))

    # Update screen
    pg.display.update()

def check_highscore(score):
    try: 
        with open('stats.json', "r+") as json_f:
            data = json.load(json_f)
            json_f.close()

            highscore = data['highscore']
            if score > highscore:
                set_highscore(score)
                print("Highscore = ", score)
                return True
    except:
        set_highscore(score)
        return True
    return False

def set_highscore(score):
    stats = {
        'player' : 'player',
        'highscore' : score, 
    }
    try:
        with open('stats.json', "w+") as json_f:
            json.dump(stats, json_f)
            json_f.close()
    except:
        print("Could not save highscore!")

def display_highscore(win):
    text = STAT_FONT.render("NEW HIGHSCORE", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH//2 - text.get_width()//2, WIN_HEIGHT//2 - text.get_height() - 5))
    pg.display.update()

def game(win):
    '''Setup and run flappy bird game'''
    score = 0
    clock = pg.time.Clock()

    # Initialize game objects
    bird = Bird(200,200)
    base = Base(730)
    pipes = [Pipe(700, score)]

    run = True

    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                bird.jump()

        bird.move()
        base.move()

        add_pipe = False
        remove_pipe = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipe.append(pipe)

            if not pipe.passed and (pipe.x + pipe.PIPE_BOTTOM.get_width()) < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700, score))

        for r in remove_pipe:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False
        
        draw_window(win, bird, pipes, base, score, run)
    
    # Display "NEW HIGHSCORE" if true
    if (check_highscore(score)):
        display_highscore(win)
        
    time.sleep(5)
    print("Game over")

    pg.quit()
    quit() 

def start():
    '''Set up pygame window and run game'''
    win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    icon = pg.image.load('flappy_bird_game/imgs/bird1.png')
    pg.display.set_icon(icon)

    game(win)

