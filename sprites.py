import pygame as pg
from settings import *
vec = pg.math.Vector2
import random
import math

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
        self.health = PLAYER_HEALTH
        self.damage_delay = 0
        self.last_attack = 0
        self.attack_state = False
        #Inicializando os retângulos de colisão de ataque
        self.attack_rect_1 = pg.Rect((0,0),(1,1))
        self.attack_rect_2 = pg.Rect((0,0),(1,1))

        self.is_dashing = False
        self.dash_frame = 0
        self.x_state = False

        self.first_collision = False

        self.inventario_x = WIDTH - 212
        self.inventario_y = HEIGHT - 474
        self.item_x = self.inventario_x + 2
        self.item_y = self.inventario_y + 142
        self.padding = 2

        self.inventario = Inventario(3,4,self.item_x,self.item_y,self.padding,self.game)
        self.inventario.add_item(Equipamento("Perna_1",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_2",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_3",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_4",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_5",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_6",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_7",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_8",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_9",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_10",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_11",10,2,5,self.game.perna_img))
        self.inventario.add_item(Equipamento("Perna_11",10,2,5,self.game.perna_img))
        self.inventario.add_item(Material("Metal",5,self.game.metal_img))
        self.chest_is_open = False

        self.interaction_state = False
        self.inv_state = False
        self.inv_active = False
        self.t_state = False
        self.esc_state = False

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
        if(not self.chest_is_open):
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
                if(not self.interaction_state):
                    self.detect_interaction()
                    self.interaction_state = True
            else:
                self.interaction_state = False

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

        if keys[pg.K_ESCAPE]:
            if(not self.esc_state):
                self.esc_state = True
                self.chest_is_open = False
        else:
            self.esc_state = False

        if keys[pg.K_i]:
            if(not self.inv_state):
                self.inv_state = True
                self.inv_active = not self.inv_active
        else:
            self.inv_state = False

        if keys[pg.K_t]:
            if(not self.t_state):
                self.t_state = True
                if(self.inv_active):
                    aux_rect = None
                    aux_ponto = pg.mouse.get_pos()
                    for i in range(self.inventario.max_linha):
                        for k in range(self.inventario.max_coluna):
                            if(i == 0):
                                if(k == 0):
                                    aux_rect = pg.Rect((self.item_x + k * ITEM_WIDTH, self.item_y + i * ITEM_HEIGHT),(ITEM_WIDTH,ITEM_HEIGHT))
                                else:
                                    aux_rect = pg.Rect((self.item_x + k * (ITEM_WIDTH + self.padding), self.item_y + i * (ITEM_HEIGHT)),(ITEM_WIDTH,ITEM_HEIGHT))
                            elif(k == 0):
                                aux_rect = pg.Rect(((self.item_x + k * ITEM_WIDTH), self.item_y + i * (ITEM_HEIGHT + self.padding)),(ITEM_WIDTH,ITEM_HEIGHT))
                            else:
                                aux_rect = pg.Rect(((self.item_x + k * (ITEM_WIDTH + self.padding)), self.item_y + i * (ITEM_HEIGHT + self.padding)),(ITEM_WIDTH,ITEM_HEIGHT))
                            if(aux_rect.collidepoint(aux_ponto)):
                                if(self.chest_is_open and not self.game.chest.inventario.is_full):
                                    #Pega o item removido do inventario do player e insire no baú
                                    aux_item = self.inventario.remove_item(i,k)
                                    #Testa se o item foi removido com sucesso
                                    if(aux_item != 0):
                                        self.game.chest.inventario.add_item(aux_item)
        else:
            self.t_state = False

    def update(self):
        if(self.health <= 0):
            self.game.new_day()
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

        #Move o Sprite e testa colisões
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        self.game.draw_rects(self.rect)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits and self.first_collision:
                if hits[0].rect.centerx > self.rect.centerx:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if hits[0].rect.centerx < self.rect.centerx:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                return 1
            if hits:
                self.first_collision = True
            return 0
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            if hits and self.first_collision:
                if hits[0].rect.centery > self.rect.centery:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if hits[0].rect.centery < self.rect.centery:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                return 1
            if hits:
                self.first_collision = True
            return 0

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
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
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
            #Testa em qual direção há objeto interagível e pega o primeiro atingido
            if(sprite.rect.collidepoint(self.pos.x - 5, self.pos.y + PLAYER_HEIGHT/2)):
                #Testa se o objeto que eu estou interagindo requer um comportamento específico
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH/2, self.pos.y - 5)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH + 5, self.pos.y + PLAYER_HEIGHT/2)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH/2, self.pos.y + PLAYER_HEIGHT + 5)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                else:
                    sprite.interaction()

    def dash_move(self):
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

    def draw_health_bar(self):
        if self.health > 60:
            cor = (0, 255, 0)
        elif self.health > 30:
            cor = (225, 225, 0)
        else:
            cor = (255, 0 ,0)
        height = int(200 * self.health/PLAYER_HEALTH)
        self.health_bar = pg.Rect(WIDTH - 60, HEIGHT - 30 - height, 30, height)
        pg.draw.rect(self.game.screen, cor, self.health_bar)

    def draw_inv(self):

        self.game.screen.blit(self.game.player_inv_img, (WIDTH - 212, HEIGHT - 474))

    #def draw_chest_inv(self):
        #if(self.chest_is_open):

#========================================================================

class SentinelaA(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.rot = 0
        self.health = 250
        self.rot_delay = 0
        self.enemy_rot_speed = ENEMY_ROT_SPEED
        self.attack_mode = False
        self.last_attack = 0

    def update(self):
        if(self.health <= 0):
            self.kill()
        if(pg.time.get_ticks() - self.rot_delay > 3500):
            self.rot_delay = pg.time.get_ticks()
            if(random.randint(1,3) == 1):
                self.enemy_rot_speed *= -1

        if(self.attack_mode):
            if(pg.time.get_ticks() - self.last_attack > 1500):
                self.last_attack = pg.time.get_ticks()
                self.attack()
        else:
            self.rot = (self.rot + self.enemy_rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.player_detection()

        aux_distancia = math.sqrt((self.pos.x - self.game.player.pos.x)**2 + (self.pos.y - self.game.player.pos.y)**2)

        if(aux_distancia > 500):
            self.attack_mode = False

    def set_damage(self, value):
        self.health -= value

    def player_detection(self):

        if(self.rot >= 45 and self.rot < 135):
            detection_rect = pg.Rect((self.pos.x - 48, self.pos.y - 64 - 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y, 1, "-x")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y, 1, "x")
        Shoot(self.game, self.pos.x, self.pos.y - ENEMY_HEIGHT, 1, "-y")
        Shoot(self.game, self.pos.x, self.pos.y + ENEMY_HEIGHT, 1, "y")

class SentinelaB(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.rot = 0
        self.health = 250
        self.rot_delay = 0
        self.enemy_rot_speed = ENEMY_ROT_SPEED
        self.attack_mode = False
        self.last_attack = 0

    def update(self):
        if(self.health <= 0):
            self.kill()
        if(pg.time.get_ticks() - self.rot_delay > 3500):
            self.rot_delay = pg.time.get_ticks()
            if(random.randint(1,3) == 1):
                self.enemy_rot_speed *= -1

        if(self.attack_mode):
            if(pg.time.get_ticks() - self.last_attack > 1500):
                self.last_attack = pg.time.get_ticks()
                self.attack()
        else:
            self.rot = (self.rot + self.enemy_rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.player_detection()

        aux_distancia = math.sqrt((self.pos.x - self.game.player.pos.x)**2 + (self.pos.y - self.game.player.pos.y)**2)

        if(aux_distancia > 500):
            self.attack_mode = False

    def set_damage(self, value):
        self.health -= value

    def player_detection(self):

        if(self.rot >= 45 and self.rot < 135):
            detection_rect = pg.Rect((self.pos.x - 48, self.pos.y - 64 - 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y, 1, "-x")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y, 1, "x")
        Shoot(self.game, self.pos.x, self.pos.y - ENEMY_HEIGHT, 1, "-y")
        Shoot(self.game, self.pos.x, self.pos.y + ENEMY_HEIGHT, 1, "y")

class SentinelaC(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.rot = 0
        self.health = 250
        self.rot_delay = 0
        self.enemy_rot_speed = ENEMY_ROT_SPEED
        self.attack_mode = False
        self.last_attack = 0

    def update(self):
        if(self.health <= 0):
            self.kill()
        if(pg.time.get_ticks() - self.rot_delay > 3500):
            self.rot_delay = pg.time.get_ticks()
            if(random.randint(1,3) == 1):
                self.enemy_rot_speed *= -1

        if(self.attack_mode):
            if(pg.time.get_ticks() - self.last_attack > 1500):
                self.last_attack = pg.time.get_ticks()
                self.attack()
        else:
            self.rot = (self.rot + self.enemy_rot_speed * self.game.dt) % 360
            self.image = pg.transform.rotate(self.game.enemy1_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.player_detection()

        aux_distancia = math.sqrt((self.pos.x - self.game.player.pos.x)**2 + (self.pos.y - self.game.player.pos.y)**2)

        if(aux_distancia > 500):
            self.attack_mode = False

    def set_damage(self, value):
        self.health -= value

    def player_detection(self):

        if(self.rot >= 45 and self.rot < 135):
            detection_rect = pg.Rect((self.pos.x - 48, self.pos.y - 64 - 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y, 3, "-x")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y, 3, "x")
        Shoot(self.game, self.pos.x, self.pos.y - ENEMY_HEIGHT, 3, "-y")
        Shoot(self.game, self.pos.x, self.pos.y + ENEMY_HEIGHT, 3, "y")

        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y + ENEMY_HEIGHT, 3, "xy")
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y + ENEMY_HEIGHT, 3, "-xy")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y - ENEMY_HEIGHT, 3, "x-y")
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y - ENEMY_HEIGHT, 3, "-x-y")

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y, area):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.boss1_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.health = 1500
        self.attack_mode = False
        self.last_attack = 0
        self.area = area

    def update(self):
        if(self.health <= 0):
            self.kill()

        if(self.attack_mode):
            if(pg.time.get_ticks() - self.last_attack > 2000):
                self.last_attack = pg.time.get_ticks()
                self.attack()
        else:
            self.player_detection()

        aux_distancia = math.sqrt((self.pos.x - self.game.player.pos.x)**2 + (self.pos.y - self.game.player.pos.y)**2)

        if(aux_distancia > 1000):
            self.attack_mode = False

    def player_detection(self):

        if(self.area == 1):
            detection_rect = pg.Rect((self.pos.x - 192, self.pos.y - 128), (192,626))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.area == 2):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.area == 3):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            self.game.draw_rects(detection_rect)
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2, self.area, "-x")
        Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 + 30, self.area, "-x")
        Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 - 30, self.area, "-x")
        Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2, self.area, "x")
        Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y + BOSS1_HEIGHT, self.area, "y")
        Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y, self.area, "-y")

    def set_damage(self, value):
        self.health -= value

class Shoot(pg.sprite.Sprite):
    def __init__(self, game, x, y, type, dir):
        self.groups = game.all_sprites, game.shoots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vel_x = 0
        self.vel_y = 0
        if(type == 1):
            if(dir == "-x"):
                self.vel_x = SHOOT_VEL * -1
                self.image = self.game.shoot1_img
            elif(dir == "x"):
                self.vel_x = SHOOT_VEL
                self.image = self.game.shoot1_img
            elif(dir == "y"):
                self.vel_y = SHOOT_VEL
                self.image = pg.transform.rotate(self.game.shoot1_img, 90)
            elif(dir == "-y"):
                self.vel_y = SHOOT_VEL * -1
                self.image = pg.transform.rotate(self.game.shoot1_img, 90)
        elif(type == 3):
            if(dir == "-x"):
                self.vel_x = SHOOT_VEL/2 * -1
                self.image = self.game.shoot3_1_img
            elif(dir == "x"):
                self.vel_x = SHOOT_VEL/2
                self.image = self.game.shoot3_1_img
            elif(dir == "y"):
                self.vel_y = SHOOT_VEL/2
                self.image = self.game.shoot3_1_img
            elif(dir == "-y"):
                self.vel_y = SHOOT_VEL/2 * -1
                self.image = self.game.shoot3_1_img
            elif(dir == "-xy"):
                self.vel_x = SHOOT_VEL/2 * -1
                self.vel_y = SHOOT_VEL/2
                self.image = self.game.shoot3_img
            elif(dir == "xy"):
                self.vel_x = SHOOT_VEL/2
                self.vel_y = SHOOT_VEL/2
                self.image = self.game.shoot3_img
            elif(dir == "x-y"):
                self.vel_x = SHOOT_VEL/2
                self.vel_y = SHOOT_VEL/2 * -1
                self.image = self.game.shoot3_img
            elif(dir == "-x-y"):
                self.vel_x = SHOOT_VEL/2 * -1
                self.vel_y = SHOOT_VEL/2 * -1
                self.image = self.game.shoot3_img


        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.spawn_time = pg.time.get_ticks()
        self.damage = SHOOT_DAMAGE

    def update(self):
        if(self.vel_x != 0):
            self.pos.x += self.vel_x * self.game.dt
        if(self.vel_y != 0):
            self.pos.y += self.vel_y * self.game.dt

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if (pg.time.get_ticks() - self.spawn_time > SHOOT_LIFE_TIME):
            self.kill()
        if(pg.sprite.collide_rect(self, self.game.player)):
            self.game.player.health -= self.damage
            self.kill()

#========================================================================

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
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

class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)
        self.inventario = Inventario(10,10,0,0,2,self.game)

    def interaction(self):
        return self.inventario

class Fence(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)

class PilhaSucata(pg.sprite.Sprite):
    def __init__(self, game, x, y, area):
        self.groups = game.respawnables, game.interactables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.pilha_sucata_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

    def interaction(self):
        print("Ganhou item!")

class PilhaFerramenta(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.respawnables, game.interactables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.pilha_ferramenta_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

    def interaction(self):
        print("Curou")

#========================================================================

class Inventario:
    def __init__(self, linhas, colunas, item_x, item_y, padding, game):
        self.game = game
        self.item_x = item_x
        self.item_y = item_y
        self.padding = padding
        self.items = []
        for x in range(linhas):
            self.items.append([])
            for y in range(colunas):
                self.items[x].append(None)

        self.max_linha = linhas
        self.max_coluna = colunas

        self.linha = 0
        self.coluna = 0

        self.is_full = False

    def add_item(self, item):
        if(not self.is_full and item != None):
            if(isinstance(item, Equipamento) or isinstance(item, Gema)):
                self.items[self.linha][self.coluna] = item
            elif(isinstance(item, Material)):
                aux_stack = 0
                for linha in self.items:
                    for coluna in linha:
                        if(coluna != None):
                            if(coluna.nome == item.nome):
                                coluna.quantidade += item.quantidade
                                aux_stack = 1
                if(aux_stack == 0):
                    self.items[self.linha][self.coluna] = item

            if(self.coluna < self.max_coluna - 1):
                self.coluna += 1
            elif(self.linha < self.max_linha - 1):
                self.linha += 1
                self.coluna = 0
            else:
                self.is_full = True

            print("")
            print("Item adicionado:")
            print(self.items)
        else:
            return 0

    def remove_item(self, l, c):
        resp = self.items[l][c]
        if(self.items[l][c] != None):
            self.items[l][c] = None
            print(self.max_coluna - 1)
            for i in range(self.max_linha):
                for j in range(self.max_coluna):
                    #Só pode começar a retirar itens e mover os outros para trás se a posição for maior que a posição do item removido
                    if(i == l):
                        if(j >= c):
                            if(j == self.max_coluna - 1):
                                if(i != self.max_linha - 1):
                                    self.items[i][j] = self.items[i + 1][0]
                                    self.items[i + 1][0] = None
                            else:
                                self.items[i][j] = self.items[i][j + 1]
                                self.items[i][j+1] = None
                    elif(i > l):
                        if(j == self.max_coluna - 1):
                            if(i != self.max_linha - 1):
                                self.items[i][j] = self.items[i + 1][0]
                                self.items[i + 1][0] = None
                        else:
                            self.items[i][j] = self.items[i][j + 1]
                            self.items[i][j+1] = None
            return resp

            print("")
            print("Item removido")
            print(self.items)

        return 0

    def print_inv(self):
        for i,linha in enumerate(self.items):
            for k,item in enumerate(linha):
                if(item != None):
                    if(i == 0):
                        if(k == 0):
                            self.game.screen.blit(item.img,(self.item_x + k * ITEM_WIDTH, self.item_y + i * ITEM_HEIGHT))
                        else:
                            self.game.screen.blit(item.img,(self.item_x + k * (ITEM_WIDTH + self.padding), self.item_y + i * (ITEM_HEIGHT)))
                    elif(k == 0):
                        self.game.screen.blit(item.img,((self.item_x + k * ITEM_WIDTH), self.item_y + i * (ITEM_HEIGHT + self.padding)))
                    else:
                        self.game.screen.blit(item.img,((self.item_x + k * (ITEM_WIDTH + self.padding)), self.item_y + i * (ITEM_HEIGHT + self.padding)))

class Equipamento:
    def __init__(self, nome, vida, dano, energia, img):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.energia = energia
        self.img = img

class Material:
    def __init__(self, nome, quantidade, img):
        self.nome = nome
        self.quantidade = quantidade
        self.img = img

class Gema:
    def __init__(self, nome, status, img):
        self.nome = nome
        self.status = status
        self.img = img
