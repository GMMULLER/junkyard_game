import pygame as pg
import random
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
        self.ground = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        enemy1_spawn_data = []

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "enemy1":
                enemy1_spawn_data.append(tile_object)

        self.spawn_enemys(enemy1_spawn_data)

        self.camera = Camera(self.map.width, self.map.height)

    def spawn_enemys(self, array):
        random.shuffle(array)
        for k, tile_object in enumerate(array):
            #Faz o spawn de metade dos inimigos
            if(k % 2 == 0):
                print("Spawn!")
                SentinelaA(self, tile_object.x, tile_object.y, random.randint(1,2))

    def load_data(self):
        #Cria as variáveis com os diretórios
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'map1.tmx'))

        #Superfície com o mapa desenhado
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()
        self.player_img_rot = pg.image.load(path.join(img_folder, PLAYER_IMAGE_ROT)).convert_alpha()

        self.enemy1_img = pg.image.load(path.join(img_folder, ENEMY1_IMG)).convert_alpha()
        self.enemy1_2_img = pg.image.load(path.join(img_folder, ENEMY1_2_IMG)).convert_alpha()


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
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

g = Game()
g.new()
g.run()
