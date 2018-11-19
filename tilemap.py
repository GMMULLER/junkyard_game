import pygame as pg
import pytmx
from settings import *

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        #Percorre todas as camadas visíveis ao jogador
        for layer in self.tmxdata.visible_layers:
            #Verifica se o Tile é um Tile do tipo Tile Layer
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        #Desenha todos eles nessa superfície
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))

    def make_map(self):
        #Instância uma superfície do mesmo tamanho do mapa
        temp_surface = pg.Surface((self.width, self.height))
        #Renderiza o mapa
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def apply_coord(self, coord_x, coord_y):
        return (coord_x + self.camera.x, coord_y + self.camera.y)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)
