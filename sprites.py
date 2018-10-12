import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        #Chamando o construtor de Sprite e passando o grupo que ele está
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #Criando a imagem do Sprite
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        #Inicializando a velocidade
        self.vel = vec(0, 0)
        #Colocando a posição inicial
        self.pos = vec(x, y) * TILESIZE
        #Ângulo de rotação da imagem (Começa virado para direita)
        self.rot_img = 0
        #Ângulo de rotação do player
        self.rot_angle = 0
        #Verifica movimentação diagonal
        self.deg_mov = False

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.rot_img = 180
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.rot_img = 0
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.rot_img = 90
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.rot_img = 270

        self.rot_angle = self.rot_img

        if self.vel.x != 0 and self.vel.y != 0:
            self.deg_mov = True
            #Dividindo pela sqrt(2) para que a movimentação na diagonal tenha a mesma velocidade
            self.vel *= 0.7071
            #Modifica o ângulo de rotação
            if(self.vel.x > 0):
                if(self.vel.y > 0):
                    #Diagonal inferior direita
                    self.rot_img = 270
                    self.rot_angle = 315
                else:
                    #Diagonal superior direita
                    self.rot_img = 0
                    self.rot_angle = 45
            else:
                if(self.vel.y > 0):
                    #Diagonal inferior esquerda
                    self.rot_img = 180
                    self.rot_angle = 225
                else:
                    #Diagonal superior esquerda
                    self.rot_img = 90
                    self.rot_angle = 135
        else:
            self.deg_mov = False

    #Reescrita da função herdada de Sprite
    def update(self):
        self.get_keys()
        #Rotaciona a imagem
        if(self.deg_mov):
            self.image = pg.transform.rotate(self.game.player_img_rot, self.rot_img)
        else:
            self.image = pg.transform.rotate(self.game.player_img, self.rot_img)
        #Muda a posição do sprite
        self.pos += self.vel * self.game.dt
        #Move o Sprite e testa colisões
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

#========================================================================

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        #Passando como parâmetro os grupos em que o Sprite está
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#========================================================================

class SwordAttack(pg.sprite.Sprite):
    def __init__(self, game, user, angle = 0):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.user = user
        self.image =  pg.Surface(50,25)
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.pos = vec()
