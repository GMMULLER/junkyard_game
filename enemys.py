import pygame as pg
from settings import *
from inventory import *
from sprites import *
vec = pg.math.Vector2
import random
import math

#Sentinelas da primeira área
class SentinelaA(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
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
            self.drop_items()
            self.kill()

        #A cada 3s e meio a sentinela pode mudar o sentido de rotação
        if(pg.time.get_ticks() - self.rot_delay > 3500):
            self.rot_delay = pg.time.get_ticks()
            if(random.randint(1,3) == 1):
                self.enemy_rot_speed *= -1

        #Entra em modo de ataque e para de rotacionar
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

        #Usa a formula de distância para calcular a distância entre a sentinela e o player
        aux_distancia = math.sqrt((self.pos.x - self.game.player.pos.x)**2 + (self.pos.y - self.game.player.pos.y)**2)

        if(aux_distancia > 500):
            self.attack_mode = False

    def set_damage(self, value):
        self.health -= value

    def player_detection(self):

        if(self.rot >= 45 and self.rot < 135):
            detection_rect = pg.Rect((self.pos.x - 48, self.pos.y - 64 - 48), (96,64))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y, 1, "-x")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y, 1, "x")
        Shoot(self.game, self.pos.x, self.pos.y - ENEMY_HEIGHT, 1, "-y")
        Shoot(self.game, self.pos.x, self.pos.y + ENEMY_HEIGHT, 1, "y")

    def drop_items(self):
        aux_inventario = self.game.player.inventario
        fio_rand = random.randint(1,3)
        fio = Material("Fio", fio_rand * 5, self.game.fio_img)
        frag_cranio_rand = random.randint(0,2)
        frag_cranio = Material("fc(T3)", frag_cranio_rand, self.game.frag_cranio_t3_img)
        frag_mand_rand = random.randint(0,2)
        frag_mand = Material("fm(T3)", frag_mand_rand, self.game.frag_mand_t3_img)

        if(self.type == 1):
            metal_rand = random.randint(1,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)

            aux_inventario.add_item(metal)

        elif(self.type == 2):
            circuito_rand = random.randint(1,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)

            aux_inventario.add_item(circuito)

        aux_inventario.add_item(fio)
        if(frag_cranio_rand != 0):
            aux_inventario.add_item(frag_cranio)
        if(frag_mand_rand != 0):
            aux_inventario.add_item(frag_mand)

#Sentinelas da segunda área
class SentinelaB(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
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
            self.drop_items()
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
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        Shoot(self.game, self.pos.x - ENEMY_WIDTH, self.pos.y - SHOOT2_HEIGHT, 2, "-x")
        Shoot(self.game, self.pos.x + ENEMY_WIDTH, self.pos.y - SHOOT2_HEIGHT, 2, "x")
        Shoot(self.game, self.pos.x - SHOOT2_WIDTH, self.pos.y - ENEMY_HEIGHT, 2, "-y")
        Shoot(self.game, self.pos.x - SHOOT2_WIDTH, self.pos.y + ENEMY_HEIGHT, 2, "y")

    def drop_items(self):
        aux_inventario = self.game.player.inventario
        parafuso_rand = random.randint(1,3)
        parafuso = Material("Parafuso", parafuso_rand * 5, self.game.parafuso_img)
        frag_braco_rand = random.randint(0,2)
        frag_braco = Material("fb(T3)", frag_braco_rand, self.game.frag_braco_t3_img)
        frag_peit_rand = random.randint(0,2)
        frag_peit = Material("fpeit(T3)", frag_peit_rand, self.game.frag_peit_t3_img)

        if(self.type == 2):
            metal_rand = random.randint(1,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)

            aux_inventario.add_item(metal)

        elif(self.type == 1):
            circuito_rand = random.randint(1,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)

            aux_inventario.add_item(circuito)

        aux_inventario.add_item(parafuso)
        if(frag_peit_rand != 0):
            aux_inventario.add_item(frag_peit)
        if(frag_braco_rand != 0):
            aux_inventario.add_item(frag_braco)

#Sentinelas da terceira área
class SentinelaC(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.enemys, game.respawnables, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
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
            self.drop_items()
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
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot < 45 or self.rot >= 315):
            detection_rect = pg.Rect((self.pos.x + ENEMY_WIDTH/2, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 135 and self.rot < 225):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2 - 64, self.pos.y - 48), (64,96))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.rot >= 225 and self.rot < 315):
            detection_rect = pg.Rect((self.pos.x - ENEMY_WIDTH/2, self.pos.y + 48), (96,64))
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

    def drop_items(self):
        aux_inventario = self.game.player.inventario
        engrenagem_rand = random.randint(1,3)
        engrenagem = Material("Engrenagem", engrenagem_rand * 5, self.game.engrenagem_img)
        frag_perna_1_rand = random.randint(0,2)
        frag_perna_1 = Material("fper1(T3)", frag_perna_1_rand, self.game.frag_perna_1_t3_img)
        frag_perna_2_rand = random.randint(0,2)
        frag_perna_2 = Material("fper2(T3)", frag_perna_2_rand, self.game.frag_perna_2_t3_img)

        if(self.type == 2):
            metal_rand = random.randint(1,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)

            aux_inventario.add_item(metal)

        elif(self.type == 1):
            circuito_rand = random.randint(1,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)

            aux_inventario.add_item(circuito)

        aux_inventario.add_item(engrenagem)
        if(frag_perna_1_rand != 0):
            aux_inventario.add_item(frag_perna_1)
        if(frag_perna_2_rand != 0):
            aux_inventario.add_item(frag_perna_2)

class Boss(pg.sprite.Sprite):
    def __init__(self, game, x, y, area):
        self.groups = game.all_sprites, game.enemys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if(area == 1 or area == 2):
            self.image = self.game.boss1_img
        elif(area == 3):
            self.image = pg.transform.rotate(self.game.boss1_img, 180)
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
            #O primeiro boss eliminado desbloqueia a habilidade de dash
            self.game.player.desb_dash = True
            self.game.desb_dash_time = pg.time.get_ticks()
            self.drop_items()
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
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.area == 2):
            detection_rect = pg.Rect((self.pos.x - 192, self.pos.y - 128), (192,626))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)
        elif(self.area == 3):
            detection_rect = pg.Rect((self.pos.x + BOSS1_WIDTH, self.pos.y - 128), (192,626))
            hit = pg.Rect.colliderect(detection_rect, self.game.player.rect)

        if(hit):
            self.attack_mode = True
            self.last_attack = pg.time.get_ticks()

    def attack(self):
        if(self.area == 1):
            aux_random = random.randint(1,5)
            if(aux_random == 1):
                for i in range(12):
                    Shoot(self.game, self.pos.x, self.pos.y - 192 + i * 64, 1, "-x")
            elif(aux_random == 2):
                for i in range(30):
                    Shoot(self.game, self.pos.x - i * 2, self.pos.y - 80, 1, "-x")
                    Shoot(self.game, self.pos.x - i * 2, self.pos.y + BOSS1_HEIGHT + 80, 1, "-x")
            else:
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2, 1, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 + 60, 1, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 - 60, 1, "-x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 - 60, 1, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2, 1, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 + 60, 1, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y + BOSS1_HEIGHT, 1, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y + BOSS1_HEIGHT, 1, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y + BOSS1_HEIGHT, 1, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y, 1, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y, 1, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y, 1, "-y")
        elif(self.area == 2):
            aux_random = random.randint(1,5)
            if(aux_random == 1):
                for i in range(12):
                    Shoot(self.game, self.pos.x, self.pos.y - 192 + i * 64, 2, "-x")
            elif(aux_random == 2):
                for i in range(30):
                    Shoot(self.game, self.pos.x - i * 2, self.pos.y - 80, 2, "-x")
                    Shoot(self.game, self.pos.x - i * 2, self.pos.y + BOSS1_HEIGHT + 80, 2, "-x")
            else:
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2, 2, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 + 60, 2, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 - 60, 2, "-x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 - 60, 2, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2, 2, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 + 60, 2, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y + BOSS1_HEIGHT, 2, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y + BOSS1_HEIGHT, 2, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y + BOSS1_HEIGHT, 2, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y, 2, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y, 2, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y, 2, "-y")
        elif(self.area == 3):
            aux_random = random.randint(1,6)
            if(aux_random == 1):
                for i in range(12):
                    Shoot(self.game, self.pos.x, self.pos.y - 192 + i * 64, 3, "x")
            elif(aux_random == 2):
                for i in range(30):
                    Shoot(self.game, self.pos.x + i * 2, self.pos.y - 80, 3, "x")
                    Shoot(self.game, self.pos.x + i * 2, self.pos.y + BOSS1_HEIGHT + 80, 3, "x")
            else:
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y, 3, "x-y")
                Shoot(self.game, self.pos.x, self.pos.y, 3, "-x-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT, 3, "xy")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT, 3, "-xy")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2, 3, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 + 60, 3, "x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH, self.pos.y + BOSS1_HEIGHT/2 - 60, 3, "x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 - 60, 3, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2, 3, "-x")
                Shoot(self.game, self.pos.x, self.pos.y + BOSS1_HEIGHT/2 + 60, 3, "-x")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y, 3, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y, 3, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y, 3, "-y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 + 60, self.pos.y + BOSS1_HEIGHT, 3, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2 - 60, self.pos.y + BOSS1_HEIGHT, 3, "y")
                Shoot(self.game, self.pos.x + BOSS1_WIDTH/2, self.pos.y + BOSS1_HEIGHT, 3, "y")

    def set_damage(self, value):
        self.health -= value

    def drop_items(self):
        aux_inventario = self.game.player.inventario
        metal = Material("Metal", 40, self.game.metal_img)
        circuito = Material("Circuito", 40, self.game.circuito_img)


        if(self.area == 1):
            fio = Material("Fio", 100, self.game.fio_img)
            frag_cranio = Material("fc(T3)", 15, self.game.frag_cranio_t3_img)
            frag_mand = Material("fm(T3)", 15, self.game.frag_mand_t3_img)
            aux_inventario.add_item(fio)
            aux_inventario.add_item(frag_cranio)
            aux_inventario.add_item(frag_mand)
            self.game.player.gem_inv.items[0][0] = Gema("gem1", self.game.gem1_img)
        elif(self.area == 2):
            parafuso = Material("Parafuso", 100, self.game.parafuso_img)
            frag_braco = Material("fb(T3)", 15, self.game.frag_braco_t3_img)
            frag_peit = Material("fpeit(T3)", 15, self.game.frag_peit_t3_img)
            aux_inventario.add_item(parafuso)
            aux_inventario.add_item(frag_braco)
            aux_inventario.add_item(frag_peit)
            self.game.player.gem_inv.items[1][0] = Gema("gem2", self.game.gem2_img)
        elif(self.area == 3):
            engrenagem = Material("Engrenagem", 100, self.game.engrenagem_img)
            frag_perna_1 = Material("fper1(T3)", 15, self.game.frag_perna_1_t3_img)
            frag_perna_2 = Material("fper2(T3)", 15, self.game.frag_perna_2_t3_img)
            aux_inventario.add_item(engrenagem)
            aux_inventario.add_item(frag_perna_1)
            aux_inventario.add_item(frag_perna_2)
            self.game.player.gem_inv.items[2][0] = Gema("gem3", self.game.gem3_img)

        aux_inventario.add_item(metal)
        aux_inventario.add_item(circuito)
        self.game.player.att_status()

class Shoot(pg.sprite.Sprite):
    def __init__(self, game, x, y, type, dir):
        self.groups = game.all_sprites, game.shoots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vel_x = 0
        self.vel_y = 0
        #Cada tipo de tiro tem possibilidades distintas de direção
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
        elif(type == 2):
            if(dir == "-x"):
                self.vel_x = SHOOT_VEL * -1
                self.image = pg.transform.rotate(self.game.shoot2_img, 90)
            elif(dir == "x"):
                self.vel_x = SHOOT_VEL
                self.image = pg.transform.rotate(self.game.shoot2_img, -90)
            elif(dir == "y"):
                self.vel_y = SHOOT_VEL
                self.image = pg.transform.rotate(self.game.shoot2_img, 180)
            elif(dir == "-y"):
                self.vel_y = SHOOT_VEL * -1
                self.image = self.game.shoot2_img
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

        #Testa se o tiro colidiu com uma parede
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        #Testa se o tempo de vida do tiro acabou
        if (pg.time.get_ticks() - self.spawn_time > SHOOT_LIFE_TIME):
            self.kill()
        #Testa se o tiro colidiu com o player
        if(pg.sprite.collide_rect(self, self.game.player)):
            self.game.player.set_damage(self.damage)
            self.kill()
