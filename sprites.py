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
        self.pos = vec(x, y)
        #Ângulo de rotação da imagem (Começa virado para direita)
        self.rot_img = 0
        #Ângulo de rotação do player
        self.rot_angle = 0
        #Verifica movimentação diagonal
        self.diag_mov = False
        #Inicializa os atributos do Player
        self.attack_power = 20
        self.life_points = 100
        self.last_attack = 0
        self.attack_state = False
        #Inicializando os retângulos de colisão de ataque
        self.attack_rect_1 = pg.Rect((0,0),(1,1))
        self.attack_rect_2 = pg.Rect((0,0),(1,1))

        self.is_dashing = False
        self.dash_frame = 0
        self.x_state = False

        self.dash = []
        contador = 1
        for i in range(0,26):
            if(i > 12):
                contador -= 55
            else:
                contador += 55
            self.dash.append(contador)

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

        if keys[pg.K_z]:
            now = pg.time.get_ticks()
            if(now - self.last_attack > PLAYER_ATTACK_RATE):
                if(not self.attack_state):
                    self.melee_attack()
                    self.attack_state = True
        else:
            self.attack_state = False

        if keys[pg.K_c]:
            self.detect_interaction()

        if keys[pg.K_x]:
            if(not self.x_state):
                self.is_dashing = True
                self.x_state = True
        else:
            self.x_state = False

        if self.vel.x != 0 and self.vel.y != 0:
            self.diag_mov = True
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
            self.diag_mov = False
            self.rot_angle = self.rot_img


    def update(self):
        if(not self.is_dashing):
            self.get_keys()
        #Rotaciona a imagem
        if(self.diag_mov):
            self.image = pg.transform.rotate(self.game.player_img_rot, self.rot_img)
        else:
            self.image = pg.transform.rotate(self.game.player_img, self.rot_img)

        #Muda a posição do sprite
        if(not self.is_dashing):
            self.pos += self.vel * self.game.dt
        else:
            self.dash_move()

        print(self.is_dashing)
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

    def melee_attack(self):
        self.last_attack = pg.time.get_ticks()

        if(self.rot_angle == 0):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width + 5,self.pos.y - self.rect.height/2),(64, 128))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
        elif(self.rot_angle == 45):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width/2, self.pos.y - 5 - self.rect.height),(32, 64))
            self.attack_rect_2 = pg.Rect((self.attack_rect_1.x + self.attack_rect_1.width + 1 ,self.attack_rect_1.y), (32, 96))
        elif(self.rot_angle == 90):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width/2, self.pos.y - 5 - 64), (128, 64))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
        elif(self.rot_angle == 135):
            self.attack_rect_1 = pg.Rect((self.pos.x, self.rect.y - self.rect.height - 5),(32, 64))
            self.attack_rect_2 = pg.Rect((self.attack_rect_1.x - self.rect.width/2 - 1, self.attack_rect_1.y), (32, 96))
        elif(self.rot_angle == 180):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width - 5, self.pos.y - self.rect.height/2), (64, 128))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
        elif(self.rot_angle == 225):
            self.attack_rect_1 = pg.Rect((self.rect.x, self.rect.y + self.rect.height + 5),(32,64))
            self.attack_rect_2 = pg.Rect((self.rect.x - self.rect.width/2, self.rect.y + self.rect.height/2),(32,101))
        elif(self.rot_angle == 270):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width/2, self.pos.y + self.rect.height + 5),(128, 64))
        elif(self.rot_angle == 315):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width/2 + 5, self.pos.y + self.rect.height + 5),(32,64))
            self.attack_rect_2 = pg.Rect((self.pos.x + self.rect.width + 5, self.pos.y + self.rect.height/2),(32,101))


        for sprite in self.game.enemys:
            if(self.attack_rect_1.width > 1):
                hit1 = pg.Rect.colliderect(self.attack_rect_1, sprite.rect)
            else:
                hit1 = 0

            if(self.attack_rect_2.width > 1):
                hit2 = pg.Rect.colliderect(self.attack_rect_2, sprite.rect)
            else:
                hit2 = 0

            if(hit1 or hit2):
                sprite.set_damage(self.attack_power)

    def detect_interaction(self):
        for sprite in self.game.interactables:
            if(sprite.rect.collidepoint(self.pos.x - 5,self.pos.y + self.rect.width)):
                sprite.interaction()

    def dash_move(self):
        #Ou seja se essa é a primeira chamada da sequência
        if(self.dash_frame < len(self.dash)):
            if(self.rot_angle == 0):
                self.pos.x += self.dash[self.dash_frame] * self.game.dt
            elif(self.rot_angle == 45):
                self.pos.x += self.dash[self.dash_frame] * self.game.dt * 0.7071
                self.pos.y -= self.dash[self.dash_frame] * self.game.dt * 0.7071
            elif(self.rot_angle == 90):
                self.pos.y -= self.dash[self.dash_frame] * self.game.dt
            elif(self.rot_angle == 135):
                self.pos.x -= self.dash[self.dash_frame] * self.game.dt * 0.7071
                self.pos.y -= self.dash[self.dash_frame] * self.game.dt * 0.7071
            elif(self.rot_angle == 180):
                self.pos.x -= self.dash[self.dash_frame] * self.game.dt
            elif(self.rot_angle == 225):
                self.pos.x -= self.dash[self.dash_frame] * self.game.dt * 0.7071
                self.pos.y += self.dash[self.dash_frame] * self.game.dt * 0.7071
            elif(self.rot_angle == 270):
                self.pos.y += self.dash[self.dash_frame] * self.game.dt
            elif(self.rot_angle == 315):
                self.pos.x += self.dash[self.dash_frame] * self.game.dt * 0.7071
                self.pos.y += self.dash[self.dash_frame] * self.game.dt * 0.7071


            self.dash_frame += 1
        else:
            self.is_dashing = False
            self.dash_frame = 0

#========================================================================

class SentinelaA(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.rot = 0
        self.life_points = 250

    def update(self):
        if(self.life_points <= 0):
            self.kill()
        self.rot = (self.rot + ENEMY_ROT_SPEED * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def set_damage(self, value):
        self.life_points -= value

class SentinelaA(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if(type == 1):
            self.image = self.game.enemy1_img
        if(type == 2):
            self.image = self.game.enemy1_2_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.rot = 0
        self.life_points = 250

    def update(self):
        if(self.life_points <= 0):
            self.kill()
        self.rot = (self.rot + ENEMY_ROT_SPEED * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def set_damage(self, value):
        self.life_points -= value

#========================================================================

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        #Passando como parâmetro os grupos em que o Sprite está
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)

class Plug(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)

    def interaction(self):
        self.game.new_day()
#========================================================================
