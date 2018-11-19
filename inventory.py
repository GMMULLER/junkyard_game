import pygame as pg
from settings import *
from sprites import *
vec = pg.math.Vector2
import random
import math

class Inventario:
    def __init__(self, linhas, colunas, item_x, item_y, padding, game, print_WIDTH, print_HEIGHT):
        self.game = game
        self.item_x = item_x
        self.item_y = item_y
        self.padding = padding
        self.items = []
        pg.font.init()
        self.myfont = pg.font.SysFont("Comic Sans Ms", 15)
        for x in range(linhas):
            self.items.append([])
            for y in range(colunas):
                self.items[x].append(None)

        self.max_linha = linhas
        self.max_coluna = colunas

        self.linha = 0
        self.coluna = 0

        self.is_full = False

        self.print_WIDTH = print_WIDTH
        self.print_HEIGHT = print_HEIGHT

    def add_item(self, item):
        print(self.linha, self.coluna)
        if(not self.is_full and item != None):
            aux_stack = 0
            if(isinstance(item, Equipamento) or isinstance(item, Gema)):
                self.items[self.linha][self.coluna] = item
            elif(isinstance(item, Material)):
                for linha in self.items:
                    for coluna in linha:
                        if(coluna != None):
                            if(coluna.nome == item.nome):
                                coluna.quantidade += item.quantidade
                                aux_stack = 1
                if(aux_stack == 0):
                    self.items[self.linha][self.coluna] = item
            if(aux_stack == 0):
                if(self.coluna < self.max_coluna - 1):
                    self.coluna += 1
                elif(self.linha < self.max_linha - 1):
                    self.linha += 1
                    self.coluna = 0
                else:
                    self.is_full = True

        else:
            return 0

    def remove_item(self, l, c):
        resp = self.items[l][c]
        if(self.items[l][c] != None):
            self.items[l][c] = None
            for i in range(self.max_linha):
                for j in range(self.max_coluna):
                    aux_remove = 0
                    #Só pode começar a retirar itens e mover os outros para trás se a posição for maior que a posição do item removido
                    if(i == l):
                        if(j >= c):
                            if(j == self.max_coluna - 1):
                                if(i != self.max_linha - 1):
                                    self.items[i][j] = self.items[i + 1][0]
                                    self.items[i + 1][0] = None
                                    aux_remove = 1
                            else:
                                self.items[i][j] = self.items[i][j + 1]
                                self.items[i][j+1] = None
                                aux_remove = 1
                    elif(i > l):
                        if(j == self.max_coluna - 1):
                            if(i != self.max_linha - 1):
                                self.items[i][j] = self.items[i + 1][0]
                                self.items[i + 1][0] = None
                                aux_remove = 1
                        else:
                            self.items[i][j] = self.items[i][j + 1]
                            self.items[i][j+1] = None
                            aux_remove = 1

            if(self.coluna != 0):
                self.coluna -= 1
            elif(self.linha != 0):
                self.coluna = self.max_coluna - 1
                self.linha -= 1

            return resp

        return 0

    def print_inv(self, image = 1):
        for i,linha in enumerate(self.items):
            for k,item in enumerate(linha):
                if(item != None):
                    #Se estiver printando os equipamentos no inventario de equipamentos deve-se usar uma imagem diferente
                    print_img = item.img
                    if(image == 2):
                        print_img = item.img2
                    if(i == 0):
                        if(k == 0):
                            self.game.screen.blit(print_img,(self.item_x + k * self.print_WIDTH, self.item_y + i * self.print_HEIGHT))
                            #Testa se o item a ser printado é do tipo material para mostrar também a quantidade
                            if(isinstance(item,Material)):
                                textsurface = self.myfont.render("Qtd: "+str(item.quantidade), False, (255,255,255))
                                self.game.screen.blit(textsurface,(self.item_x + k * self.print_WIDTH, self.item_y + i * self.print_HEIGHT))
                        else:
                            self.game.screen.blit(print_img,(self.item_x + k * (self.print_WIDTH + self.padding), self.item_y + i * (self.print_HEIGHT)))
                            if(isinstance(item,Material)):
                                textsurface = self.myfont.render("Qtd: "+str(item.quantidade), False, (255,255,255))
                                self.game.screen.blit(textsurface,(self.item_x + k * (self.print_WIDTH + self.padding), self.item_y + i * (self.print_HEIGHT)))
                    elif(k == 0):
                        self.game.screen.blit(print_img,((self.item_x + k * self.print_WIDTH), self.item_y + i * (self.print_HEIGHT + self.padding)))
                        if(isinstance(item,Material)):
                            textsurface = self.myfont.render("Qtd: "+str(item.quantidade), False, (255,255,255))
                            self.game.screen.blit(textsurface,((self.item_x + k * self.print_WIDTH), self.item_y + i * (self.print_HEIGHT + self.padding)))
                    else:
                        self.game.screen.blit(print_img,((self.item_x + k * (self.print_WIDTH + self.padding)), self.item_y + i * (self.print_HEIGHT + self.padding)))
                        if(isinstance(item,Material)):
                            textsurface = self.myfont.render("Qtd: "+str(item.quantidade), False, (255,255,255))
                            self.game.screen.blit(textsurface,((self.item_x + k * (self.print_WIDTH + self.padding)), self.item_y + i * (self.print_HEIGHT + self.padding)))

    def set_empty(self):
        for i in range(self.max_linha):
            for k in range(self.max_coluna):
                self.items[i][k] = None

        self.linha = 0
        self.coluna = 0

#Por enquanto os materiais e equipamentos são reconhecidos pelo nome e não por um id
class Equipamento:
    def __init__(self, nome, vida, dano, energia, img1, img2 = None, quantidade = 1):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.energia = energia
        self.img = img1
        if(img2 != None):
            self.img2 = img2
        else:
            self.img2 = img1
        self.quantidade = quantidade

class Material:
    def __init__(self, nome, quantidade, img):
        self.nome = nome
        self.quantidade = quantidade
        self.img = img

class Gema:
    def __init__(self, nome, img, quantidade = 1):
        self.nome = nome
        self.img = img
        self.quantidade = quantidade
