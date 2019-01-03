import pygame as pg
from settings import *
from inventory import *
from enemys import *
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
        self.vel_bonus = 1
        #Ângulo de rotação da imagem (Começa virado para direita)
        self.rot_img = 0
        #Ângulo de rotação do player
        self.rot_angle = 0
        #Verifica movimentação diagonal
        self.diag_mov = False
        #Inicializa os atributos do Player
        self.attack_power = PLAYER_ATTACK_DAM
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.max_energy = PLAYER_ENERGY
        self.energy = self.max_energy
        #Variáveis para atacar
        self.damage_delay = 0
        self.last_attack = 0
        self.attack_state = False
        self.attack_rate = PLAYER_ATTACK_RATE
        self.deny_damage = False
        self.attack_anim_frame = 0
        self.attacking = False
        #Inicializando os retângulos de colisão de ataque
        self.attack_rect_1 = pg.Rect((0,0),(1,1))
        self.attack_rect_2 = pg.Rect((0,0),(1,1))

        #Variáveis para o dash
        self.is_dashing = False
        self.dash_frame = 0
        self.dash = []
        self.desb_dash = False

        #Variável para correção de bug
        self.first_collision = False

        #Inventário
        self.inventario_x = WIDTH - PLAYER_INV_WIDTH - 30
        self.inventario_y = 30
        self.item_x = self.inventario_x + 2
        self.item_y = self.inventario_y + 142
        self.padding = 2
        self.inv_active = False
        self.inventario = Inventario(3,4,self.item_x,self.item_y,self.padding,self.game, ITEM_WIDTH, ITEM_HEIGHT)
        self.inventario.add_item(Equipamento("ht3", 150, 0, 0, self.game.head_t3, self.game.head_equip_t3))
        self.inventario.add_item(Equipamento("pt3", 0, 100, 0, self.game.chest_t3, self.game.chest_equip_t3))
        self.inventario.add_item(Equipamento("lt3", 0, 0, 100, self.game.leg_t3, self.game.leg_equip_t3))
        self.inventario.add_item(Equipamento("ht1", 15, 0, 0, self.game.head_t1, self.game.head_equip_t1))

        #Inventários que o Player interage
        self.chest_is_open = False
        self.table_is_open = False
        self.equip_inv = Inventario(3,1, self.inventario_x + 116, self.inventario_y + 2, self.padding, self.game, EQUIP_WIDTH, EQUIP_HEIGHT)
        self.gem_inv = Inventario(3,1, self.inventario_x + 168, self.inventario_y + 2, self.padding, self.game, GEM_WIDTH, GEM_HEIGHT)

        #Pilha
        self.searching = False
        self.sch_cont = 0

        #Estador do teclado
        self.t_state = False
        self.esc_state = False
        self.e_state = False
        self.x_state = False
        self.interaction_state = False
        self.inv_state = False

        #Frames da animação de ataque
        self.attack_frames = [self.game.attack_anim_1,self.game.attack_anim_2,self.game.attack_anim_3,self.game.attack_anim_4,self.game.attack_anim_5]

        self.myfont = pg.font.SysFont("Comic Sans Ms", 18)

        #Cria um vetor de velocidades para dar efeito de aceleração no dash
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
        can_mov = False
    
        #Testa se o Player pode se mover
        if(not self.chest_is_open):
            if(not self.table_is_open):
                if(not self.searching):
                    if(not (self.game.generator.gen_msg and not self.game.generator.drew_msg)):
                        if(not self.game.alc_msg):
                            can_mov = True

        if(can_mov):
            #Movimentação
            if keys[pg.K_LEFT]:
                self.vel.x = -PLAYER_SPEED
                self.rot_img = 180
            if keys[pg.K_RIGHT]:
                self.vel.x = PLAYER_SPEED
                self.rot_img = 0
            if keys[pg.K_UP]:
                self.vel.y = -PLAYER_SPEED
                self.rot_img = 90
            if keys[pg.K_DOWN]:
                self.vel.y = PLAYER_SPEED
                self.rot_img = 270

            #Ataque
            if keys[pg.K_z]:
                now = pg.time.get_ticks()
                if(now - self.last_attack > self.attack_rate):
                    if(not self.attack_state):
                        self.melee_attack()
                        self.attack_state = True
            else:
                self.attack_state = False

            #Interação
            if keys[pg.K_x]:
                if(not self.interaction_state):
                    self.detect_interaction()
                    self.interaction_state = True
            else:
                self.interaction_state = False

            #Testa se o dash foi desbloqueado
            if(self.desb_dash):
                if keys[pg.K_c]:
                    if(not self.x_state):
                        self.is_dashing = True
                        self.x_state = True
                else:
                    self.x_state = False

            #Testa se o Player está fazendo um movimento diagonal
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

        #Tecla usada para fechar as abas de inventário
        if keys[pg.K_ESCAPE]:
            if(not self.esc_state):
                self.esc_state = True
                self.chest_is_open = False
                self.table_is_open = False
                #Quando a mensagem do gerador é fechada atualiza-se a variável para ela nunca mais aparecer
                if(self.game.generator.gen_msg):
                    self.game.generator.drew_msg = True
                self.game.generator.gen_msg = False
                self.game.alc_msg = False
        else:
            self.esc_state = False

        #Abre o inventário do Player
        if keys[pg.K_i]:
            if(not self.inv_state):
                self.inv_state = True
                self.inv_active = not self.inv_active
        else:
            self.inv_state = False

        #Faz as interações no inventário do Player
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
                    #Testa se o mouse do jogador está sobre determinada parte do inventário
                    if(aux_rect.collidepoint(aux_ponto)):
                        #Faz o item ser transferido do inventário do Player para o Baú
                        if keys[pg.K_t]:
                            if(not self.t_state):
                                self.t_state = True
                                if(self.chest_is_open and not self.game.chest.inventario.is_full):
                                    #Pega o item removido do inventario do player e insere no baú
                                    aux_item = self.inventario.remove_item(i,k)
                                    #Testa se o item foi removido com sucesso
                                    if(aux_item != 0):
                                        self.inventario.is_full = False
                                        self.game.chest.inventario.add_item(aux_item)
                        else:
                            self.t_state = False
                            #Tecla e para equipar itens que estão no inventário
                            if keys[pg.K_e]:
                                if(not self.e_state):
                                    self.e_state = True
                                    #Só equipamentos são equipáveis
                                    if(isinstance(self.inventario.items[i][k],Equipamento)):
                                        aux_equip = self.inventario.items[i][k]
                                        #Como o inventário de equipamentos é praticamento um vetor cada tipo de item tem seu lugar correto
                                        if(aux_equip.nome == "ht1" or aux_equip.nome == "ht2" or aux_equip.nome == "ht3"):
                                            if(self.equip_inv.items[0][0] == None):
                                                self.equip_inv.items[0][0] = aux_equip
                                                self.inventario.remove_item(i,k)
                                        elif(aux_equip.nome == "pt1" or aux_equip.nome == "pt2" or aux_equip.nome == "pt3"):
                                            if(self.equip_inv.items[1][0] == None):
                                                self.equip_inv.items[1][0] = aux_equip
                                                self.inventario.remove_item(i,k)
                                        elif(aux_equip.nome == "lt1" or aux_equip.nome == "lt2" or aux_equip.nome == "lt3"):
                                            if(self.equip_inv.items[2][0] == None):
                                                self.equip_inv.items[2][0] = aux_equip
                                                self.inventario.remove_item(i,k)
                                        #Depois de trocar de equipamento faz as devidas atualizações nos atributos do Player
                                        self.att_status()
                            else:
                                self.e_state = False

            for i in range(self.equip_inv.max_linha):
                for k in range(self.equip_inv.max_coluna):
                    if(i == 0):
                        if(k == 0):
                            aux_rect = pg.Rect((self.equip_inv.item_x + k * EQUIP_WIDTH, self.equip_inv.item_y + i * EQUIP_HEIGHT),(EQUIP_WIDTH,EQUIP_HEIGHT))
                        else:
                            aux_rect = pg.Rect((self.equip_inv.item_x + k * (EQUIP_WIDTH + self.equip_inv.padding), self.equip_inv.item_y + i * (EQUIP_HEIGHT)),(EQUIP_WIDTH,EQUIP_HEIGHT))
                    elif(k == 0):
                        aux_rect = pg.Rect(((self.equip_inv.item_x + k * EQUIP_WIDTH), self.equip_inv.item_y + i * (EQUIP_HEIGHT + self.equip_inv.padding)),(EQUIP_WIDTH,EQUIP_HEIGHT))
                    else:
                        aux_rect = pg.Rect(((self.equip_inv.item_x + k * (EQUIP_WIDTH + self.equip_inv.padding)), self.equip_inv.item_y + i * (EQUIP_HEIGHT + self.equip_inv.padding)),(EQUIP_WIDTH,EQUIP_HEIGHT))
                    if(aux_rect.collidepoint(aux_ponto)):
                        if keys[pg.K_e]:
                            if(not self.e_state):
                                self.e_state = True
                                if(not self.inventario.is_full):
                                    #Tira items do inventário de equipamento e coloca no inventário do Player
                                    self.inventario.add_item(self.equip_inv.items[i][k])
                                    self.equip_inv.items[i][k] = None
                                    self.att_status()
                        else:
                            self.e_state = False

            aux_rect = None
            self.chest = self.game.chest
            if(self.chest_is_open):
                for i in range(self.chest.inventario.max_linha):
                    for k in range(self.chest.inventario.max_coluna):
                        if(i == 0):
                            if(k == 0):
                                aux_rect = pg.Rect((self.chest.item_x + k * ITEM_WIDTH, self.chest.item_y + i * ITEM_HEIGHT),(ITEM_WIDTH,ITEM_HEIGHT))
                            else:
                                aux_rect = pg.Rect((self.chest.item_x + k * (ITEM_WIDTH + self.padding), self.chest.item_y + i * (ITEM_HEIGHT)),(ITEM_WIDTH,ITEM_HEIGHT))
                        elif(k == 0):
                            aux_rect = pg.Rect(((self.chest.item_x + k * ITEM_WIDTH), self.chest.item_y + i * (ITEM_HEIGHT + self.padding)),(ITEM_WIDTH,ITEM_HEIGHT))
                        else:
                            aux_rect = pg.Rect(((self.chest.item_x + k * (ITEM_WIDTH + self.padding)), self.chest.item_y + i * (ITEM_HEIGHT + self.padding)),(ITEM_WIDTH,ITEM_HEIGHT))
                        if(aux_rect.collidepoint(aux_ponto)):
                            if keys[pg.K_t]:
                                if(not self.t_state):
                                    self.t_state = True
                                    if(self.inv_active and not self.inventario.is_full):
                                        #Pega o item removido do inventario do baú e insere no do player
                                        aux_item = self.chest.inventario.remove_item(i,k)
                                        #Testa se o item foi removido com sucesso
                                        if(aux_item != 0):
                                            self.chest.inventario.is_full = False
                                            self.inventario.add_item(aux_item)
                            else:
                                self.t_state = False

        if keys[pg.K_e]:
            if(not self.e_state):
                self.e_state = True
                self.game.table.mouse_test()
        else:
            self.e_state = False

    def update(self):
        if(self.health <= 0 or self.energy <= 0):
            self.inventario.set_empty()
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
            self.pos += self.vel * self.game.dt * self.vel_bonus
        else:
            self.dash_move()

        #Move o Sprite e testa colisões
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

    def collide_with_walls(self, dir):
        #Faz colisão parcial com respeito ao x
        if dir == 'x':
            #Retorna todos os sprites de wall que estão colidindo com o Player
            hits = pg.sprite.spritecollide(self,self.game.walls, False)
            #Correção de bug
            if hits and self.first_collision:
                #Reposiciona o Player
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
        #Faz colisão parcial com respeito ao y
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
        #Monta os rects de teste de colisão de acordo com a direção que o Player está
        self.last_attack = pg.time.get_ticks()
        if(self.rot_angle == 0):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width + 5,self.pos.y - self.rect.height/2),(64, 128))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
            self.attacking = True
        elif(self.rot_angle == 45):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width/2, self.pos.y - 5 - self.rect.height),(32, 64))
            self.attack_rect_2 = pg.Rect((self.attack_rect_1.x + self.attack_rect_1.width + 1 ,self.attack_rect_1.y), (32, 96))
            self.attacking = True
        elif(self.rot_angle == 90):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width/2, self.pos.y - 5 - 64), (128, 64))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
            self.attacking = True
        elif(self.rot_angle == 135):
            self.attack_rect_1 = pg.Rect((self.pos.x, self.rect.y - self.rect.height - 5),(32, 64))
            self.attack_rect_2 = pg.Rect((self.attack_rect_1.x - self.rect.width/2 - 1, self.attack_rect_1.y), (32, 96))
            self.attacking = True
        elif(self.rot_angle == 180):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width - 5, self.pos.y - self.rect.height/2), (64, 128))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
            self.attacking = True
        elif(self.rot_angle == 225):
            self.attack_rect_1 = pg.Rect((self.rect.x, self.rect.y + self.rect.height + 5),(32,64))
            self.attack_rect_2 = pg.Rect((self.rect.x - self.rect.width/2, self.rect.y + self.rect.height/2),(32,101))
            self.attacking = True
        elif(self.rot_angle == 270):
            self.attack_rect_1 = pg.Rect((self.pos.x - self.rect.width/2, self.pos.y + self.rect.height + 5),(128, 64))
            self.attack_rect_2 = pg.Rect((0,0),(1,1))
            self.attacking = True
        elif(self.rot_angle == 315):
            self.attack_rect_1 = pg.Rect((self.pos.x + self.rect.width/2 + 5, self.pos.y + self.rect.height + 5),(32,64))
            self.attack_rect_2 = pg.Rect((self.pos.x + self.rect.width + 5, self.pos.y + self.rect.height/2),(32,101))
            self.attacking = True


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

        self.energy -= 2

    def detect_interaction(self):
        for sprite in self.game.interactables:
            #Testa em qual direção há objeto interagível e pega o primeiro atingido
            if(sprite.rect.colliderect(self.rect)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                elif(isinstance(sprite, Working_Table)):
                    self.table_is_open = True
                    sprite.interaction()
                elif(isinstance(sprite, PilhaSucata) or isinstance(sprite, PilhaFerramenta)):
                    self.pilha_atual = sprite
                    sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x - 10, self.pos.y + PLAYER_HEIGHT/2)):
                #Testa se o objeto que eu estou interagindo requer um comportamento específico
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                elif(isinstance(sprite, Working_Table)):
                    self.table_is_open = True
                    sprite.interaction()
                elif(isinstance(sprite, PilhaSucata) or isinstance(sprite, PilhaFerramenta)):
                    self.pilha_atual = sprite
                    sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH/2, self.pos.y - 10)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                elif(isinstance(sprite, Working_Table)):
                    self.table_is_open = True
                    sprite.interaction()
                elif(isinstance(sprite, PilhaSucata) or isinstance(sprite, PilhaFerramenta)):
                    self.pilha_atual = sprite
                    sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH + 10, self.pos.y + PLAYER_HEIGHT/2)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                elif(isinstance(sprite, Working_Table)):
                    self.table_is_open = True
                    sprite.interaction()
                elif(isinstance(sprite, PilhaSucata) or isinstance(sprite, PilhaFerramenta)):
                    self.pilha_atual = sprite
                    sprite.interaction()
                else:
                    sprite.interaction()
            elif(sprite.rect.collidepoint(self.pos.x + PLAYER_WIDTH/2, self.pos.y + PLAYER_HEIGHT + 10)):
                if(isinstance(sprite, Chest)):
                    self.chest_is_open = True
                    self.chest_inv = sprite.interaction()
                elif(isinstance(sprite, Working_Table)):
                    self.table_is_open = True
                    sprite.interaction()
                elif(isinstance(sprite, PilhaSucata) or isinstance(sprite, PilhaFerramenta)):
                    self.pilha_atual = sprite
                    sprite.interaction()
                else:
                    sprite.interaction()

    def dash_move(self):
        #Dependendo da direção do Player a posição é incrementada de maneira distinta
        if(self.dash_frame < len(self.dash)):
            if(self.rot_angle == 0):
                self.pos.x += self.dash[self.dash_frame] * self.game.dt
            elif(self.rot_angle == 45):
                #Constante serve para fazer com que o movimento na diagonal seja na mesma velocidade que os outros
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
            self.energy -= 5
            self.is_dashing = False
            self.dash_frame = 0

    def draw_health_bar(self):
        #Testa qual cor deve ser exibida
        if self.health > 6/10 * self.max_health:
            cor = (0, 255, 0)
        elif self.health > 3/10 * self.max_health:
            cor = (225, 225, 0)
        else:
            cor = (255, 0 ,0)
        #Calcula quantos por cento da vida máxima o Player tem e a altura da barra que possui no máximo 200 pixels
        height = int(200 * self.health/self.max_health)
        self.health_bar = pg.Rect(WIDTH - 120, HEIGHT - 30 - height, 30, height)
        pg.draw.rect(self.game.screen, cor, self.health_bar)
        aux_text = str(self.health)+"/"+str(self.max_health)
        textsurface = self.myfont.render(aux_text, False, (0,255,0))
        self.game.screen.blit(textsurface,(WIDTH - 120 - 12, HEIGHT - 30 - height - 20))

    def draw_energy_bar(self):
        height = int(200 * self.energy/self.max_energy)
        self.energy_bar = pg.Rect(WIDTH - 60, HEIGHT - 30 - height, 30, height)
        pg.draw.rect(self.game.screen, (0, 0, 255), self.energy_bar)
        aux_text = str(self.energy)+"/"+str(self.max_energy)
        textsurface = self.myfont.render(aux_text, False, (0,0,255))
        self.game.screen.blit(textsurface,(WIDTH - 60 - 12, HEIGHT - 30 - height - 20))

    def draw_inv(self):
        self.game.screen.blit(self.game.player_inv_img, (WIDTH - PLAYER_INV_WIDTH - 30, 30))

    def att_status(self):
        energia = 0
        ataque = 0
        vida = 0
        for i in self.equip_inv.items:
            for item in i:
                if item != None:
                    energia += item.energia
                    ataque += item.dano
                    vida += item.vida

        self.max_health = PLAYER_HEALTH + vida
        self.max_energy = PLAYER_ENERGY + energia
        self.attack_power = PLAYER_ATTACK_DAM + ataque

        if(self.health > self.max_health):
            self.health = self.max_health
        if(self.energy > self.max_energy):
            self.energy = self.max_energy

        #Aplica os efeitos das gemas dos Bosses
        if(self.gem_inv.items[0][0] != None):
            self.attack_rate = PLAYER_ATTACK_RATE/2
        if(self.gem_inv.items[1][0] != None):
            self.deny_damage = True
        if(self.gem_inv.items[2][0] != None):
            self.vel_bonus = 1.5

    def draw_sch_bar(self):
        width = int(200 * self.sch_cont/100)
        aux_sch_bar = pg.Rect(WIDTH/2 - 100, HEIGHT - 40, width, 30)
        pg.draw.rect(self.game.screen, (0,0,255), aux_sch_bar)
        if(self.sch_cont >= 100):
            self.energy -= 3
            self.searching = False
            self.sch_cont = 0
            self.pilha_atual.drop_items()
        self.sch_cont += 60 * self.game.dt

    def set_damage(self, damage):
        if(self.deny_damage):
            aux_random = random.randint(1,4)
            if(aux_random != 4):
                self.health -= damage
        else:
            self.health -= damage

#Áreas intransponíveis do mapa
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
        self.inventario_x = WIDTH/2 - CHEST_INV_WIDTH/2
        self.inventario_y = HEIGHT/2 - CHEST_INV_HEIGHT/2
        self.inv_padding = 2
        self.item_x = self.inventario_x + self.inv_padding
        self.item_y = self.inventario_y + self.inv_padding
        self.inventario = Inventario(10,10,self.item_x,self.item_y,self.inv_padding,self.game, ITEM_WIDTH, ITEM_HEIGHT)

    def interaction(self):
        return self.inventario

    def draw_inv(self):
        self.game.screen.blit(self.game.chest_inv_img, (self.inventario_x, self.inventario_y))

class Working_Table(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)
        self.padding = 3

        #Recursos recessários para fabricar cada item
        self.head_t1 = {"Metal":20,"Fio":35,"fc(T1)":15,"fm(T1)":15,"Parafuso":35,"Engrenagem":35}
        self.head_t2 = {"Circuito":35,"Fio":60,"fc(T2)":25,"fm(T2)":25,"Parafuso":60,"Engrenagem":60}
        self.head_t3 = {"Metal":60,"Fio":120,"fc(T3)":30,"fm(T3)":30,"Parafuso":120,"Engrenagem":120}

        self.chest_t1 = {"Circuito":20,"Fio":35,"fb(T1)":15,"fpeit(T1)":15,"Parafuso":35,"Engrenagem":35}
        self.chest_t2 = {"Metal":35,"Fio":60,"fb(T2)":25,"fpeit(T2)":25,"Parafuso":60,"Engrenagem":60}
        self.chest_t3 = {"Circuito":60,"Fio":120,"fb(T3)":30,"fpeit(T3)":30,"Parafuso":120,"Engrenagem":120}

        self.leg_t1 = {"Metal":20,"Fio":35,"fper1(T1)":15,"fper2(T1)":15,"Parafuso":35,"Engrenagem":35}
        self.leg_t2 = {"Circuito":35,"Fio":60,"fper1(T2)":25,"fper2(T2)":25,"Parafuso":60,"Engrenagem":60}
        self.leg_t3 = {"Metal":60,"Fio":120,"fper1(T3)":30,"fper2(T3)":30,"Parafuso":120,"Engrenagem":120}

        self.crafting_data = [[self.head_t1,self.head_t2,self.head_t3],[self.chest_t1,self.chest_t2,self.chest_t3],[self.leg_t1,self.leg_t2,self.leg_t3]]

        self.e_state = False

    def interaction(self):
        return 0

    def draw_table(self):
        self.game.screen.blit(self.game.working_table_img, (WIDTH/2 - WORKING_TABLE_WIDTH/2, HEIGHT/2 - WORKING_TABLE_HEIGHT/2))

    def mouse_test(self):
        #Testando se o mouse do player está sobre uma janela de craft
        keys = pg.key.get_pressed()
        aux_ponto = pg.mouse.get_pos()
        self.table_x = WIDTH/2 - WORKING_TABLE_WIDTH/2
        self.table_y = HEIGHT/2 - WORKING_TABLE_HEIGHT/2
        self.first_craft_x = self.table_x + 3
        self.first_craft_y = self.table_y + 29
        if(self.game.player.table_is_open):
            for i in range(3):
                for k in range(3):
                    if(i == 0):
                        if(k == 0):
                            aux_rect = pg.Rect((self.first_craft_x + k * CRAFT_TILE_WIDTH, self.first_craft_y + i * CRAFT_TILE_HEIGHT),(CRAFT_TILE_WIDTH,CRAFT_TILE_HEIGHT))
                        else:
                            aux_rect = pg.Rect((self.first_craft_x + k * (CRAFT_TILE_WIDTH + self.padding), self.first_craft_y + i * (CRAFT_TILE_HEIGHT)),(CRAFT_TILE_WIDTH,CRAFT_TILE_HEIGHT))
                    elif(k == 0):
                        aux_rect = pg.Rect(((self.first_craft_x + k * CRAFT_TILE_WIDTH), self.first_craft_y + i * (CRAFT_TILE_HEIGHT + self.padding)),(CRAFT_TILE_WIDTH,CRAFT_TILE_HEIGHT))
                    else:
                        aux_rect = pg.Rect(((self.first_craft_x + k * (CRAFT_TILE_WIDTH + self.padding)), self.first_craft_y + i * (CRAFT_TILE_HEIGHT + self.padding)),(CRAFT_TILE_WIDTH,CRAFT_TILE_HEIGHT))
                    if(aux_rect.collidepoint(aux_ponto)):
                        if keys[pg.K_e]:
                            if(not self.e_state):
                                self.e_state = True
                                aux_can_craft = []
                                aux_inv = self.game.player.inventario
                                for x in range(aux_inv.max_linha):
                                    for y in range(aux_inv.max_coluna):
                                        #Pega a quantidade de determinado material do inventário do Player que precisa para produzir o item que o mouse está sobre
                                        if(aux_inv.items[x][y] != None):
                                            aux_material = self.crafting_data[i][k].get(aux_inv.items[x][y].nome)
                                            if(aux_material != None):
                                                #Testa se a quantidade do material no inventário do Player supre a necessidade requerida
                                                if(aux_inv.items[x][y].quantidade >= aux_material):
                                                    aux_can_craft.append(1)
                                                else:
                                                    aux_can_craft.append(0)
                                #Cada equipamento requer 6 tipos de itens distintos
                                can_craft = True
                                if(len(aux_can_craft) == 6):
                                    for test in aux_can_craft:
                                        #Se faltar um item não é possível produzir
                                        if(test == 0):
                                            can_craft = False
                                            break
                                else:
                                    can_craft = False

                                if(can_craft):
                                    aux_equip = None
                                    if(i == 0 and k == 0):
                                        aux_equip = Equipamento("ht1", 15, 0, 0, self.game.head_t1, self.game.head_equip_t1)
                                    elif(i == 0 and k == 1):
                                        aux_equip = Equipamento("ht2", 50, 0, 0, self.game.head_t2, self.game.head_equip_t2)
                                    elif(i == 0 and k == 2):
                                        aux_equip = Equipamento("ht3", 150, 0, 0, self.game.head_t3, self.game.head_equip_t3)
                                    elif(i == 1 and k == 0):
                                        aux_equip = Equipamento("pt1", 0, 20, 0, self.game.chest_t1, self.game.chest_equip_t1)
                                    elif(i == 1 and k == 1):
                                        aux_equip = Equipamento("pt2", 0, 30, 0, self.game.chest_t2, self.game.chest_equip_t2)
                                    elif(i == 1 and k == 2):
                                        aux_equip = Equipamento("pt3", 0, 100, 0, self.game.chest_t3, self.game.chest_equip_t3)
                                    elif(i == 2 and k == 0):
                                        aux_equip = Equipamento("lt1", 0, 0, 10, self.game.leg_t1, self.game.leg_equip_t1)
                                    elif(i == 2 and k == 1):
                                        aux_equip = Equipamento("lt2", 0, 0, 30, self.game.leg_t2, self.game.leg_equip_t2)
                                    elif(i == 2 and k == 2):
                                        aux_equip = Equipamento("lt3", 0, 0, 100, self.game.leg_t3, self.game.leg_equip_t3)

                                    if(aux_inv.add_item(aux_equip) != 0):
                                        for n,linha in enumerate(aux_inv.items):
                                            for m,item in enumerate(linha):
                                                if(item != None):
                                                    #A função get() retorna nulo se o item não precisa desse material
                                                    aux_material = self.crafting_data[i][k].get(item.nome)
                                                    if(aux_material != None):
                                                        item.quantidade -= aux_material

                                        for n,linha in enumerate(aux_inv.items):
                                            for m,item in enumerate(linha):
                                                #Só remover e cotinuar a interação faz com que um item com quantidade 0 possa ser deslocado para a posição anterior da próxima iteração do for
                                                if(item != None):
                                                    while(aux_inv.items[n][m].quantidade == 0):
                                                        aux_inv.remove_item(n,m)
                                                        if(aux_inv.items[n][m] == None):
                                                            break
                        else:
                            self.e_state = False

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
        self.area = area
        self.image = self.game.pilha_sucata_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

    def interaction(self):
        self.game.player.searching = True

    def drop_items(self):
        aux_inventario = self.game.player.inventario

        if(self.area == 1):
            frag_cranio_rand = random.randint(0,1)
            frag_cranio = Material("fc(T1)", frag_cranio_rand, self.game.frag_cranio_img)
            if(frag_cranio_rand != 0):
                aux_inventario.add_item(frag_cranio)

            frag_mand_rand = random.randint(0,1)
            frag_mand = Material("fm(T1)", frag_mand_rand, self.game.frag_mand_img)
            if(frag_mand_rand != 0):
                aux_inventario.add_item(frag_mand)

            frag_cranio_rand = random.randint(0,1)
            frag_cranio = Material("fc(T2)", frag_cranio_rand, self.game.frag_cranio_t2_img)
            if(frag_cranio_rand != 0):
                aux_inventario.add_item(frag_cranio)

            frag_mand_rand = random.randint(0,1)
            frag_mand = Material("fm(T2)", frag_mand_rand, self.game.frag_mand_t2_img)
            if(frag_mand_rand != 0):
                aux_inventario.add_item(frag_mand)

            fio_rand = random.randint(0,1)
            fio = Material("Fio", fio_rand * 5, self.game.fio_img)
            if(fio_rand != 0):
                aux_inventario.add_item(fio)

            metal_rand = random.randint(0,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)
            if(metal_rand != 0):
                aux_inventario.add_item(metal)

            circuito_rand = random.randint(0,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)
            if(circuito_rand != 0):
                aux_inventario.add_item(circuito)

        elif(self.area == 2):
            aux_inventario = self.game.player.inventario

            parafuso_rand = random.randint(0,3)
            parafuso = Material("Parafuso", parafuso_rand * 5, self.game.parafuso_img)
            if(parafuso_rand != 0):
                aux_inventario.add_item(parafuso)

            frag_braco_rand = random.randint(0,1)
            frag_braco = Material("fb(T1)", frag_braco_rand, self.game.frag_braco_img)
            if(frag_braco_rand != 0):
                aux_inventario.add_item(frag_braco)

            frag_peit_rand = random.randint(0,1)
            frag_peit = Material("fpeit(T1)", frag_peit_rand, self.game.frag_peit_img)
            if(frag_peit_rand != 0):
                aux_inventario.add_item(frag_peit)

            frag_braco_rand = random.randint(0,1)
            frag_braco = Material("fb(T2)", frag_braco_rand, self.game.frag_braco_t2_img)
            if(frag_braco_rand != 0):
                aux_inventario.add_item(frag_braco)

            frag_peit_rand = random.randint(0,1)
            frag_peit = Material("fpeit(T2)", frag_peit_rand, self.game.frag_peit_t2_img)
            if(frag_peit_rand != 0):
                aux_inventario.add_item(frag_peit)

            metal_rand = random.randint(0,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)
            if(metal_rand != 0):
                aux_inventario.add_item(metal)

            circuito_rand = random.randint(0,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)
            if(metal_rand != 0):
                aux_inventario.add_item(metal)

        elif(self.area == 3):
            aux_inventario = self.game.player.inventario

            engrenagem_rand = random.randint(0,3)
            engrenagem = Material("Engrenagem", engrenagem_rand * 5, self.game.engrenagem_img)
            if(engrenagem_rand != 0):
                aux_inventario.add_item(engrenagem)

            frag_perna_1_rand = random.randint(0,1)
            frag_perna_1 = Material("fper1(T1)", frag_perna_1_rand, self.game.frag_perna_1_img)
            if(frag_perna_1_rand != 0):
                aux_inventario.add_item(frag_perna_1)

            frag_perna_2_rand = random.randint(0,1)
            frag_perna_2 = Material("fper2(T1)", frag_perna_2_rand, self.game.frag_perna_2_img)
            if(frag_perna_2_rand != 0):
                aux_inventario.add_item(frag_perna_2)

            frag_perna_1_rand = random.randint(0,1)
            frag_perna_1 = Material("fper1(T2)", frag_perna_1_rand, self.game.frag_perna_1_t2_img)
            if(frag_perna_1_rand != 0):
                aux_inventario.add_item(frag_perna_1)

            frag_perna_2_rand = random.randint(0,1)
            frag_perna_2 = Material("fper2(T2)", frag_perna_2_rand, self.game.frag_perna_2_t2_img)
            if(frag_perna_2_rand != 0):
                aux_inventario.add_item(frag_perna_2)

            metal_rand = random.randint(0,3)
            metal = Material("Metal", metal_rand * 2, self.game.metal_img)
            if(metal_rand != 0):
                aux_inventario.add_item(metal)

            circuito_rand = random.randint(0,3)
            circuito = Material("Circuito", circuito_rand * 2, self.game.circuito_img)
            if(circuito_rand != 0):
                aux_inventario.add_item(circuito)

        self.kill()

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
        self.game.player.searching = True

    def drop_items(self):
        #Testa se a cura ultrapassará a vida máxima do Player
        if(self.game.player.health + 30 >= self.game.player.max_health):
            self.game.player.health = self.game.player.max_health
        else:
            self.game.player.health += 30

        self.kill()

class Gerador(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.drew_msg = False
        self.gen_msg = False
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)
        self.myfont = pg.font.SysFont("Comic Sans Ms", 30)

    def interaction(self):
        #Flag para indicar que a menssagem do gerador deve ser exibida
        self.gen_msg = True

    def draw_message(self):
        textsurface = self.myfont.render("* O gerador voltou a funcionar! *", False, (255,255,255))
        self.game.screen.blit(textsurface,(WIDTH/2 - 130,HEIGHT - 30))

class Alcapao(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.pos = vec(x, y)
        self.myfont = pg.font.SysFont("Comic Sans Ms", 30)

    def interaction(self):
        self.game.alc_msg = True
        aux_gem = self.game.player.gem_inv
        #Testa se o Player possui todas as gemas para abrir o alçapão
        if(aux_gem.items[0][0] != None and aux_gem.items[1][0] != None and aux_gem.items[2][0] != None):
            #Entra em um loop em que é exibido uma tela de congratulações
            while(1):
                self.game.screen.fill((0,0,0))
                self.game.screen.blit(self.game.gameover_img, (WIDTH/2 - 426, HEIGHT/2 - 240))
                keys = pg.key.get_pressed()
                pg.display.flip()
                if keys[pg.K_ESCAPE]:
                    self.game.running = False
                    pg.quit()
                    break
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        pg.quit()
                        break
