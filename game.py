import pygame as pg
import random
from settings import *
from sprites import *
from tilemap import *
from inventory import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.day = 0
        pg.font.init()
        self.myfont = pg.font.SysFont("Comic Sans Ms", 30)
        self.player = None
        self.inv_state = False
        self.drew_desb_dash = False
        self.desb_dash_time = 0
        self.alc_msg = False

    def new(self):
        self.day = 1
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.ground = pg.sprite.Group()
        self.enemys = pg.sprite.Group()
        self.interactables = pg.sprite.Group()
        self.shoots = pg.sprite.Group()
        self.respawnables = pg.sprite.Group()
        self.enemy1_spawn_data = []
        self.enemy2_spawn_data = []
        self.enemy3_spawn_data = []
        self.pilhas1_sucata = []
        self.pilhas2_sucata = []
        self.pilhas3_sucata = []
        self.pilhas1_ferramenta = []
        self.pilhas2_ferramenta = []
        self.pilhas3_ferramenta = []

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "enemy1":
                self.enemy1_spawn_data.append(tile_object)
            if tile_object.name == "enemy2":
                self.enemy2_spawn_data.append(tile_object)
            if tile_object.name == "enemy3":
                self.enemy3_spawn_data.append(tile_object)
            if tile_object.name == "plug":
                Plug(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "fence":
                Fence(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "pilha_sucata_1":
                self.pilhas1_sucata.append(tile_object)
            if tile_object.name == "pilha_sucata_2":
                self.pilhas2_sucata.append(tile_object)
            if tile_object.name == "pilha_sucata_3":
                self.pilhas3_sucata.append(tile_object)
            if tile_object.name == "boss1":
                Boss(self, tile_object.x, tile_object.y, 1)
            if tile_object.name == "boss2":
                Boss(self, tile_object.x, tile_object.y, 2)
            if tile_object.name == "boss3":
                Boss(self, tile_object.x, tile_object.y, 3)
            if tile_object.name == "pilha_ferramenta_1":
                self.pilhas1_ferramenta.append(tile_object)
            if tile_object.name == "pilha_ferramenta_2":
                self.pilhas2_ferramenta.append(tile_object)
            if tile_object.name == "pilha_ferramenta_3":
                self.pilhas3_ferramenta.append(tile_object)
            if tile_object.name == "chest":
                self.chest = Chest(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "working":
                self.table = Working_Table(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "generator":
                self.generator = Gerador(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "trapdoor":
                Alcapao(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.spawn_enemys(self.enemy1_spawn_data, 1)
        self.spawn_enemys(self.enemy2_spawn_data, 2)
        self.spawn_enemys(self.enemy3_spawn_data, 3)
        self.spawn_pilhas_sucata(self.pilhas1_sucata, 1)
        self.spawn_pilhas_sucata(self.pilhas2_sucata, 2)
        self.spawn_pilhas_sucata(self.pilhas3_sucata, 3)
        self.spawn_pilhas_ferramenta(self.pilhas1_ferramenta)
        self.spawn_pilhas_ferramenta(self.pilhas2_ferramenta)
        self.spawn_pilhas_ferramenta(self.pilhas3_ferramenta)

        self.camera = Camera(self.map.width, self.map.height)

    def spawn_enemys(self, array, area):
        random.shuffle(array)
        for k, tile_object in enumerate(array):
            #Faz o spawn de metade dos inimigos
            if(k % 2 == 0):
                if(area == 1):
                    SentinelaA(self, tile_object.x, tile_object.y, random.randint(1,2))
                if(area == 2):
                    SentinelaB(self, tile_object.x, tile_object.y, random.randint(1,2))
                if(area == 3):
                    SentinelaC(self, tile_object.x, tile_object.y, random.randint(1,2))

    def spawn_pilhas_sucata(self, array, area):
        random.shuffle(array)
        for k, tile_object in enumerate(array):
            if(k % 2 == 0):
                    PilhaSucata(self, tile_object.x, tile_object.y, area)

    def spawn_pilhas_ferramenta(self, array):
        random.shuffle(array)
        for k, tile_object in enumerate(array):
            if(k % 2 == 0):
                PilhaFerramenta(self, tile_object.x, tile_object.y)

    def new_day(self):
        self.day += 1
        self.player.health = self.player.max_health
        self.player.energy = self.player.max_energy

        for sprite in self.respawnables:
            sprite.kill()

        self.spawn_enemys(self.enemy1_spawn_data, 1)
        self.spawn_enemys(self.enemy2_spawn_data, 2)
        self.spawn_enemys(self.enemy3_spawn_data, 3)
        self.spawn_pilhas_sucata(self.pilhas1_sucata, 1)
        self.spawn_pilhas_sucata(self.pilhas2_sucata, 2)
        self.spawn_pilhas_sucata(self.pilhas3_sucata, 3)
        self.spawn_pilhas_ferramenta(self.pilhas1_ferramenta)
        self.spawn_pilhas_ferramenta(self.pilhas2_ferramenta)
        self.spawn_pilhas_ferramenta(self.pilhas3_ferramenta)

        for sprite in self.interactables:
            if(isinstance(sprite, Plug)):
                self.plug = sprite
                break

        self.player.pos.x = self.plug.pos.x
        self.player.pos.y = self.plug.pos.y + 2 + self.plug.rect.height

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

        self.shoot1_img = pg.image.load(path.join(img_folder, SHOOT1_SPRITE)).convert_alpha()
        self.shoot2_img = pg.image.load(path.join(img_folder, SHOOT2_SPRITE)).convert_alpha()
        self.shoot3_img = pg.image.load(path.join(img_folder, SHOOT3_SPRITE)).convert_alpha()
        self.shoot3_1_img = pg.image.load(path.join(img_folder, SHOOT3_1_SPRITE)).convert_alpha()

        self.pilha_sucata_img = pg.image.load(path.join(img_folder, PILHA_SUCATA_IMG)).convert_alpha()
        self.pilha_ferramenta_img = pg.image.load(path.join(img_folder, PILHA_FERRAMENTA_IMG)).convert_alpha()

        self.boss1_img = pg.image.load(path.join(img_folder, BOSS1_IMG)).convert_alpha()

        self.player_inv_img = pg.image.load(path.join(img_folder, PLAYER_INV_IMG)).convert_alpha()
        self.chest_inv_img = pg.image.load(path.join(img_folder, CHEST_INV_IMG)).convert_alpha()

        self.metal_img = pg.image.load(path.join(img_folder, METAL_IMG)).convert_alpha()
        self.circuito_img = pg.image.load(path.join(img_folder, CIRCUITO_IMG)).convert_alpha()
        self.engrenagem_img = pg.image.load(path.join(img_folder, ENGRENAGEM_IMG)).convert_alpha()
        self.parafuso_img = pg.image.load(path.join(img_folder, PARAFUSO_IMG)).convert_alpha()
        self.fio_img = pg.image.load(path.join(img_folder, FIO_IMG)).convert_alpha()
        self.frag_mand_img = pg.image.load(path.join(img_folder, FRAG_MAND_IMG)).convert_alpha()
        self.frag_cranio_img = pg.image.load(path.join(img_folder, FRAG_CRANIO_IMG)).convert_alpha()
        self.frag_braco_img = pg.image.load(path.join(img_folder, FRAG_BRACO_IMG)).convert_alpha()
        self.frag_peit_img = pg.image.load(path.join(img_folder, FRAG_PEIT_IMG)).convert_alpha()
        self.frag_perna_1_img = pg.image.load(path.join(img_folder, FRAG_PERNA_1_IMG)).convert_alpha()
        self.frag_perna_2_img = pg.image.load(path.join(img_folder, FRAG_PERNA_2_IMG)).convert_alpha()

        self.working_table_img = pg.image.load(path.join(img_folder, WORKING_TABLE_IMG)).convert_alpha()

        self.head_t1 = pg.image.load(path.join(img_folder, HEAD_T1)).convert_alpha()
        self.head_t2 = pg.image.load(path.join(img_folder, HEAD_T2)).convert_alpha()
        self.head_t3 = pg.image.load(path.join(img_folder, HEAD_T3)).convert_alpha()

        self.chest_t1 = pg.image.load(path.join(img_folder, CHEST_T1)).convert_alpha()
        self.chest_t2 = pg.image.load(path.join(img_folder, CHEST_T2)).convert_alpha()
        self.chest_t3 = pg.image.load(path.join(img_folder, CHEST_T3)).convert_alpha()

        self.leg_t1 = pg.image.load(path.join(img_folder, LEG_T1)).convert_alpha()
        self.leg_t2 = pg.image.load(path.join(img_folder, LEG_T2)).convert_alpha()
        self.leg_t3 = pg.image.load(path.join(img_folder, LEG_T3)).convert_alpha()

        self.head_equip_t1 = pg.image.load(path.join(img_folder, HEAD_EQUIP_T1)).convert_alpha()
        self.head_equip_t2 = pg.image.load(path.join(img_folder, HEAD_EQUIP_T2)).convert_alpha()
        self.head_equip_t3 = pg.image.load(path.join(img_folder, HEAD_EQUIP_T3)).convert_alpha()

        self.chest_equip_t1 = pg.image.load(path.join(img_folder, CHEST_EQUIP_T1)).convert_alpha()
        self.chest_equip_t2 = pg.image.load(path.join(img_folder, CHEST_EQUIP_T2)).convert_alpha()
        self.chest_equip_t3 = pg.image.load(path.join(img_folder, CHEST_EQUIP_T3)).convert_alpha()

        self.leg_equip_t1 = pg.image.load(path.join(img_folder, LEG_EQUIP_T1)).convert_alpha()
        self.leg_equip_t2 = pg.image.load(path.join(img_folder, LEG_EQUIP_T2)).convert_alpha()
        self.leg_equip_t3 = pg.image.load(path.join(img_folder, LEG_EQUIP_T3)).convert_alpha()

        self.gem1_img = pg.image.load(path.join(img_folder, GEM1_IMG)).convert_alpha()
        self.gem2_img = pg.image.load(path.join(img_folder, GEM2_IMG)).convert_alpha()
        self.gem3_img = pg.image.load(path.join(img_folder, GEM3_IMG)).convert_alpha()

        self.desb_dash_img = pg.image.load(path.join(img_folder, DESB_DASH_IMG)).convert_alpha()

        self.gameover_img = pg.image.load(path.join(img_folder, GAMEOVER_IMG)).convert_alpha()

        self.attack_anim_1 = pg.image.load(path.join(img_folder, ATTACK_ANIM_1_IMG)).convert_alpha()
        self.attack_anim_2 = pg.image.load(path.join(img_folder, ATTACK_ANIM_2_IMG)).convert_alpha()
        self.attack_anim_3 = pg.image.load(path.join(img_folder, ATTACK_ANIM_3_IMG)).convert_alpha()
        self.attack_anim_4 = pg.image.load(path.join(img_folder, ATTACK_ANIM_4_IMG)).convert_alpha()
        self.attack_anim_5 = pg.image.load(path.join(img_folder, ATTACK_ANIM_5_IMG)).convert_alpha()

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
        self.enemys.update()
        self.camera.update(self.player)

        if(pg.time.get_ticks() - self.player.damage_delay > 1500):
            hits = pg.sprite.spritecollide(self.player, self.enemys, False)
            for hit in hits:
                self.player.damage_delay = pg.time.get_ticks()
                self.player.set_damage(10)

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.player.draw_health_bar()

        self.player.draw_energy_bar()

        if(self.player.inv_active):
            self.player.draw_inv()
            self.player.inventario.print_inv()
            self.player.equip_inv.print_inv(2)
            self.player.gem_inv.print_inv()

        if(self.player.chest_is_open):
            self.chest.draw_inv()
            self.chest.inventario.print_inv()

        if(self.player.table_is_open):
            self.table.draw_table()

        if(self.player.searching):
            self.player.draw_sch_bar()

        if(self.generator.gen_msg and not self.generator.drew_msg):
            self.generator.draw_message()

        if(not self.drew_desb_dash and self.player.desb_dash):
            self.screen.blit(self.desb_dash_img, (30, HEIGHT - 128 - 30))
            if(pg.time.get_ticks() - self.desb_dash_time > 2000):
                self.drew_desb_dash = True

        if(self.player.attacking):
            if(self.player.rot_angle == 0):
                self.screen.blit(self.player.attack_frames[self.player.attack_anim_frame//5], self.camera.apply_coord(self.player.pos.x + 32, self.player.pos.y - 32))
            elif(self.player.rot_angle == 90):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 90), self.camera.apply_coord(self.player.pos.x - 32, self.player.pos.y - 96))
            elif(self.player.rot_angle == 180):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 180), self.camera.apply_coord(self.player.pos.x - 96, self.player.pos.y - 32))
            elif(self.player.rot_angle == 270):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 270), self.camera.apply_coord(self.player.pos.x - 32, self.player.pos.y + 32))
            elif(self.player.rot_angle == 45):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 45), self.camera.apply_coord(self.player.pos.x - 32, self.player.pos.y - 96))
            elif(self.player.rot_angle == 135):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 135), self.camera.apply_coord(self.player.pos.x - 96, self.player.pos.y - 96))
            elif(self.player.rot_angle == 225):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 225), self.camera.apply_coord(self.player.pos.x - 96, self.player.pos.y))
            elif(self.player.rot_angle == 315):
                self.screen.blit(pg.transform.rotate(self.player.attack_frames[self.player.attack_anim_frame//5], 315), self.camera.apply_coord(self.player.pos.x, self.player.pos.y - 32))

            self.player.attack_anim_frame += 1
            if(self.player.attack_anim_frame//5 > 4):
                self.player.attacking = False
                self.player.attack_anim_frame = 0

        if(self.alc_msg):
            textsurface = self.myfont.render("* Você observa 3 encaixes estranhos *", False, (255,255,255))
            self.screen.blit(textsurface,(WIDTH/2 - 130, HEIGHT - 30))


        textsurface = self.myfont.render('Dia: '+str(self.day), False, (255,255,255))

        self.screen.blit(textsurface,(10,10))

        pg.display.flip()

g = Game()
g.new()
g.run()
