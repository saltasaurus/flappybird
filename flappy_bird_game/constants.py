import pygame as pg
import os

pg.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

IMG_PATH = "flappy_bird_game/imgs"

BIRD_IMGS = [pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "bird1.png"))), 
             pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "bird2.png"))),
             pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "bird3.png")))]

PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "base.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join(IMG_PATH, "bg.png")))

STAT_FONT = pg.font.SysFont("comicsons", 50)

FPS = 30