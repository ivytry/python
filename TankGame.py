#coding:utf-8
import pygame, time
from sys import exit
from pygame.locals import *
from random import randint
__author__ = {
    'name' : 'Ivy',
    'mail' : '526560484@qq.com',
    'Version' : '1.0'
}

class TankMain:
    width = 900
    height = 600
    panel_height = 55
    grade = 1
    screen = None
    my_tank = None
    stop = False
    help = False
    help_rect = {
        "left": 0,
        "top": 0,
        "width": 0,
        "height": 0
    }

    machine_tanks = pygame.sprite.Group()
    my_tank_missile_list = []
    machine_tank_missile_list = pygame.sprite.Group()
    walls = []
    explode_list = []
    player = {}


    def __init__(self, player = {"name": "player","grade": 1}):
        TankMain.player = player
        TankMain.grade = player["grade"]
        self.background = pygame.image.load("images/bg.jpg")

        pygame.init()

        TankMain.screen = pygame.display.set_mode([TankMain.width, TankMain.height], 0)
        pygame.display.set_caption("Tank Game")

        TankMain.walls.append(Wall(100, 120))
        self.init_player_tank()

        for i in range(1, 6):
            TankMain.machine_tanks.add(MachineTank())

    def gameStart(self):
        while True:
            TankMain.screen.fill((40, 120, 30))
            TankMain.screen.blit(self.background, (0, TankMain.panel_height))

            for w in TankMain.walls:
                w.display()
                w.hit_other()

            self.write_text()
            self.get_event()

            if TankMain.my_tank:
                if TankMain.my_tank.live:
                    TankMain.my_tank.hit_me()
                    TankMain.my_tank.display()
                    TankMain.my_tank.move()
                else:
                    TankMain.my_tank = None

            for machine_tank in TankMain.machine_tanks:
                machine_tank.display()
                machine_tank.random_move()
                machine_tank.random_fire()

            for m in TankMain.machine_tank_missile_list:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.machine_tank_missile_list.remove(m)

            for missile in TankMain.my_tank_missile_list:
                if missile.live:
                    missile.display()
                    missile.move()
                    missile.hit_tank()
                else:
                    TankMain.my_tank_missile_list.remove(missile)

            for explode in TankMain.explode_list:
                explode.display()

            if TankMain.help:
                self.game_help()

            if not TankMain.my_tank or len(TankMain.machine_tanks) == 0:
                self.game_over()

            time.sleep(0.05)
            pygame.display.update()

    def init_player_tank(self):
        TankMain.my_tank = PlayerTank(TankMain.width/2 - 25, TankMain.height - 3*TankMain.panel_height)

    def gameEnd(self):
        exit()

    def write_text(self):
        font = pygame.font.SysFont("arial", 18)
        color = (250, 250, 250)
        space = 5

        if TankMain.my_tank:
            live = TankMain.my_tank.live
        else:
            live = 0

        text_life = font.render("%s's life : %d"%(TankMain.player["name"], live), True, color)
        base_rect = text_life.get_rect()
        base_rect.top = 5
        base_rect.left = 5
        TankMain.screen.blit(text_life, base_rect)

        if TankMain.my_tank:
            pygame.draw.rect(TankMain.screen, (200, 100, 0), (base_rect.left+base_rect.width+space, base_rect.top, 20 * TankMain.my_tank.live, base_rect.height))

        text_tanks = font.render("machine tank : %s"%len(TankMain.machine_tanks), True, color)
        TankMain.screen.blit(text_tanks, (base_rect.left, base_rect.top + base_rect.height + space))

        text_grade = font.render("player grade : %d"%TankMain.player['grade'], True, color)
        TankMain.screen.blit(text_grade, (TankMain.width - text_grade.get_rect().width - space, base_rect.top))

        help = font.render("help", True,(200, 200, 200))
        TankMain.help_rect["left"] = TankMain.width - help.get_rect().width - space
        TankMain.help_rect["top"] = base_rect.top + base_rect.height + space
        TankMain.help_rect["width"] = help.get_rect().width
        TankMain.help_rect["height"] = help.get_rect().height
        TankMain.screen.blit(help, (TankMain.help_rect["left"], TankMain.help_rect["top"]))

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.gameEnd()
            if event.type == KEYDOWN:
                if TankMain.my_tank:
                    if event.key == K_LEFT or event.key == K_a:
                        TankMain.my_tank.direction = "L"
                        TankMain.my_tank.stop = False
                    if event.key == K_RIGHT or event.key == K_d:
                        TankMain.my_tank.direction = "R"
                        TankMain.my_tank.stop = False
                    if event.key == K_UP or event.key == K_w:
                        TankMain.my_tank.direction = "U"
                        TankMain.my_tank.stop = False
                    if event.key == K_DOWN or event.key == K_s:
                        TankMain.my_tank.direction = "D"
                        TankMain.my_tank.stop = False
                    if event.key == K_SPACE:
                        m = TankMain.my_tank.fire()
                        m.good = True
                        TankMain.my_tank_missile_list.append(m)
                if event.key == K_ESCAPE:
                    self.gameEnd()
                if event.key == K_n and (not TankMain.my_tank):
                    self.init_player_tank()
                if event.key == K_p:
                    if TankMain.stop:
                        TankMain.stop = False
                    else:
                        TankMain.stop = True
            if event.type == KEYUP:
                if TankMain.my_tank and (event.key == K_LEFT or event.key == K_a or event.key == K_RIGHT or event.key == K_d or event.key == K_UP or event.key == K_w or event.key == K_DOWN or event.key == K_s):
                    TankMain.my_tank.stop = True
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] <= (TankMain.help_rect["left"]+TankMain.help_rect["width"]) and pos[0] >= TankMain.help_rect["left"] and pos[1] >= TankMain.help_rect["top"] and pos[1] <= (TankMain.help_rect["top"]+TankMain.help_rect["height"]):
                    TankMain.help = True
                    TankMain.stop = True
                else:
                    TankMain.help = False
                    TankMain.stop = False

    def game_help(self):
        subscreen = self.screen.subsurface((TankMain.width/4, TankMain.height/4, TankMain.width/2, TankMain.height/2))
        subscreen.fill((40, 120, 30))

        font = pygame.font.SysFont("arial", 18)
        texts = [
            font.render("keyword up/w: change direction to up", True, (250, 250, 250)),
            font.render("keyword down/s: change direction to down", True, (250, 250, 250)),
            font.render("keyword left/a: change direction to left", True, (250, 250, 250)),
            font.render("keyword right/d: change direction to right", True, (250, 250, 250)),
            font.render("keyword space: to shut the others", True, (250, 250, 250)),
            font.render("keyword n: get new life", True, (250, 250, 250)),
            font.render("keyword p: to pause", True, (250, 250, 250)),
            font.render("keyword r: to restart", True, (250, 250, 250)),
            font.render("keyword esc: to exit", True, (250, 250, 250))
        ]

        for s in texts:
            text_rect = s.get_rect()
            subscreen.blit(s, (20, 15+30*texts.index(s), text_rect.width, text_rect.height))

    def game_over(self):
        subscreen = self.screen.subsurface((TankMain.width/3, TankMain.height/3, TankMain.width/3, TankMain.height/3))
        subscreen.fill((40, 120, 30))

        font = pygame.font.SysFont("arial", 18)
        texts = []
        if TankMain.my_tank and len(TankMain.machine_tanks) == 0:
            texts = [
                font.render("You Win!", True, (250, 250, 250)),
                font.render("press keyword l to start next level", True, (250, 50, 50))
            ]
        if not TankMain.my_tank and len(TankMain.machine_tanks) > 0:
            texts = [
                font.render("Game Over!", True, (250, 250, 250)),
                font.render("press keyword r to restart again", True, (250, 50, 50))
            ]

        for s in texts:
            text_rect = s.get_rect()
            subscreen.blit(s, (TankMain.width/6-text_rect.width/2, TankMain.height/8+30*texts.index(s), text_rect.width, text_rect.height))

class BaseObj(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.live = True

    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            TankMain.screen.blit(self.image, self.rect)

class Tank(BaseObj):
    width = 50
    height = 50

    def __init__(self, left, top):
        super().__init__()
        self.direction = "D"
        self.step = 10
        self.images = {}
        self.images["L"] = pygame.image.load("images/tankL.gif")
        self.images["R"] = pygame.image.load("images/tankR.gif")
        self.images["U"] = pygame.image.load("images/tankU.gif")
        self.images["D"] = pygame.image.load("images/tankD.gif")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.stop = True
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    def move(self):
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

        if not self.stop and not TankMain.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.step
                else:
                    self.rect.left = 0
            if self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.step
                else:
                    self.rect.right = TankMain.width
            if self.direction == "U":
                if self.rect.top > TankMain.panel_height:
                    self.rect.top -= self.step
                else:
                    self.rect.top = TankMain.panel_height
            if self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.step
                else:
                    self.rect.bottom = TankMain.height

    def fire(self):
        m = Missile(self)
        return m

class PlayerTank(Tank):
    def __init__(self, left, top):
        super().__init__(left, top)
        self.live = 5

    def hit_me(self):
        hit_list = pygame.sprite.spritecollide(self, TankMain.machine_tank_missile_list, False)
        for m in hit_list:
            m.live = False
            TankMain.machine_tank_missile_list.remove(m)
            if self.live:
                self.live -= 1
            explode = Explode(self.rect)
            TankMain.explode_list.append(explode)

class MachineTank(Tank):
    def __init__(self):
        super().__init__(randint(1, TankMain.width), randint(TankMain.panel_height, TankMain.height/2))
        self.step = 5
        self.rand_step = randint(6, 10)
        self.get_rand_direction()
        self.images["L"] = pygame.image.load("images/MtankL.gif")
        self.images["R"] = pygame.image.load("images/MtankR.gif")
        self.images["U"] = pygame.image.load("images/MtankU.gif")
        self.images["D"] = pygame.image.load("images/MtankD.gif")

    def random_move(self):
        if self.live and not TankMain.stop:
            if self.rand_step == 0:
                self.get_rand_direction()
                self.rand_step = randint(6, 10)
            else:
                self.move()
                self.rand_step -= 1

    def random_fire(self):
        r = randint(0, 10)
        if not r:
            m = self.fire()
            TankMain.machine_tank_missile_list.add(m)

    def get_rand_direction(self):
        r = randint(0, 4)
        if r == 0:
            self.stop = True
        elif r == 1:
            self.direction = "L"
            self.stop = False
        elif r == 2:
            self.direction = "R"
            self.stop = False
        elif r == 3:
            self.direction = "U"
            self.stop = False
        elif r == 4:
            self.direction = "D"
            self.stop = False

class Missile(BaseObj):
    width = 10
    height = 10

    def __init__(self, tank):
        super().__init__()
        self.tank = tank
        self.direction = tank.direction
        self.step = 16
        self.images = {}
        self.images["L"] = pygame.image.load("images/missileL.gif")
        self.images["R"] = pygame.image.load("images/missileR.gif")
        self.images["U"] = pygame.image.load("images/missileU.gif")
        self.images["D"] = pygame.image.load("images/missileD.gif")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + ( tank.width - Missile.width ) / 2
        self.rect.top = tank.rect.top + ( tank.height - Missile.height ) / 2
        self.live = True
        self.good = False

    def move(self):
        if self.live and not TankMain.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.step
                else:
                    self.live = False
            if self.direction == "R":
                if self.rect.left < TankMain.width:
                    self.rect.left += self.step
                else:
                    self.live = False
            if self.direction == "U":
                if self.rect.top > TankMain.panel_height:
                    self.rect.top -= self.step
                else:
                    self.live = False
            if self.direction == "D":
                if self.rect.top < TankMain.height:
                    self.rect.top += self.step
                else:
                    self.live = False

    def hit_tank(self):
        if self.good:
            hit_list = pygame.sprite.spritecollide(self, TankMain.machine_tanks, True)
            for e in hit_list:
                e.live = False
                TankMain.machine_tanks.remove(e)
                self.live = False
                explode = Explode(e.rect)
                TankMain.explode_list.append(explode)

class Wall(BaseObj):
    def __init__(self, left, top):
        super().__init__()
        self.image = pygame.image.load("images/wood.gif")
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

    def display(self):
        TankMain.screen.blit(self.image, self.rect)

    def hit_other(self):
        if TankMain.my_tank:
            hited = pygame.sprite.spritecollide(TankMain.my_tank, TankMain.walls, False)
            if hited:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()
        if len(TankMain.machine_tanks) > 0:
            for w in TankMain.walls:
                hit_list = pygame.sprite.spritecollide(w, TankMain.machine_tanks, False)
                if len(hit_list) > 0:
                    for i in hit_list:
                        i.stop = True
                        i.stay()
        if len(TankMain.machine_tank_missile_list) > 0:
            for w in TankMain.walls:
                hit_list = pygame.sprite.spritecollide(w, TankMain.machine_tank_missile_list, False)
                if len(hit_list) > 0:
                    for i in hit_list:
                        TankMain.machine_tank_missile_list.remove(i)
        if len(TankMain.my_tank_missile_list) > 0:
            for w in TankMain.walls:
                hit_list = pygame.sprite.spritecollide(w, TankMain.my_tank_missile_list, False)
                if len(hit_list) > 0:
                    for i in hit_list:
                        TankMain.my_tank_missile_list.remove(i)

class Explode(BaseObj):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.images = [
            pygame.image.load("images/0.gif"),
            pygame.image.load("images/1.gif"),
            pygame.image.load("images/2.gif"),
            pygame.image.load("images/3.gif"),
            pygame.image.load("images/4.gif"),
            pygame.image.load("images/5.gif"),
            pygame.image.load("images/6.gif"),
            pygame.image.load("images/7.gif"),
            pygame.image.load("images/8.gif"),
            pygame.image.load("images/9.gif"),
            pygame.image.load("images/10.gif")
        ]
        self.step = 0

    def display(self):
        if self.live:
            for i in self.images:
                if self.step == len(self.images):
                    self.step = 0
                    self.live = False
                else:
                    self.image = self.images[self.step]
                    TankMain.screen.blit(self.image, self.rect)
                    self.step += 1

class Grade(BaseObj):
    def __init__(self):
        super().__init__()

        self.player_live = 5
        self.player_speed = 10
        self.player_missile_speed = 10

        self.machine_number = 5
        self.machine_live = 1
        self.machine_speed = 10
        self.machine_missile_speed = 10

        self.wall_number = 1
        self.wall_type = "wood"

    def grade_init(self):
        if TankMain.grade > 1:
            self.wall_number = 2
        if TankMain.grade > 2:
            self.machine_number = 6
        if TankMain.grade > 3:
            self.machine_speed = 20
            self.player_speed = 20
        if TankMain.grade > 4:
            self.machine_missile_speed = 20
            self.player_missile_speed = 20
        return {
            "player_live":self.player_live,
            "player_speed":self.player_speed,
            "player_missile_speed":self.player_missile_speed,
            "machine_number":self.machine_number,
            "machine_live":self.machine_live,
            "machine_speed":self.machine_speed,
            "machine_missile_speed":self.machine_missile_speed,
            "wall_number":self.wall_number,
            "wall_type":self.wall_type
        }

if __name__ == '__main__':
    ivy = {
        "name": "ivy",
        "grade": 2
    }
    game=TankMain(ivy)
    game.gameStart()
