import pygame as pg
from settings import *
from sprites import *
from tilemap import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self,col,row)
                if tile == 'P':
                    self.player = Player(self,col,row)
        self.camera = Camera(self.map.width, self.map.height)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()
        self.player_img_rot = pg.image.load(path.join(img_folder, PLAYER_IMAGE_ROT)).convert_alpha()

    def run(self):
        self.running = True
        while(self.running):
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill((0,0,0))
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,(100,100,100),(x,0),(x,HEIGHT))
        for y in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,(100,100,100),(0,y),(WIDTH,y))

g = Game()
g.new()
g.run()
