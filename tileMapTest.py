import pygame, sys
from pygame.locals import *
from PPlay.window import *

CORNER = 0
WALL = 1

#Constantes para definir o tamanho de cada tile
TILESIZE = 40
MAPWIDTH = 3
MAPHEIGHT = 5

#Dicionário para linkar os recursos as imagens
texturas = {
    CORNER : pygame.image.load('corner1.png'),
    WALL : pygame.image.load('wall.png')
}

tilemap = [
            [CORNER, CORNER, CORNER],
            [WALL, CORNER, WALL],
            [WALL, CORNER, WALL],
            [WALL, CORNER, WALL],
            [CORNER, CORNER, CORNER]
          ]

#==============================================================

#Inicializando os módulos do pygame
pygame.init()

#Criando a janela
janela = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    for linha in range(MAPHEIGHT):
        for coluna in range(MAPWIDTH):
            janela.blit(texturas[tilemap[linha][coluna]], (coluna*TILESIZE, linha*TILESIZE))

    pygame.display.update()
