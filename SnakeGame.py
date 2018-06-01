import pygame,time,math
from sys import exit
from random import randint
from pygame.locals import *

class SnakeMain:

    def __init__(self, player = {"player":"player", "grade":1}):
        SnakeMain.width = 720
        SnakeMain.height = 480
        SnakeMain.panel_height = 60
        self.food = None
        SnakeMain.help = False
        SnakeMain.stop = False
        SnakeMain.help_rect = {
            "left": 0,
            "top": 0,
            "width": 0,
            "height": 0
        }
        SnakeMain.body = []

        pygame.init()
        SnakeMain.player = player
        self.food_number = 10*SnakeMain.player["grade"]

        SnakeMain.screen = pygame.display.set_mode([SnakeMain.width, SnakeMain.height], 0)
        pygame.display.set_caption("Snake Game")

        SnakeMain.snake = Head((math.floor(SnakeMain.width/2 - 6)/12)*12, math.floor((SnakeMain.height - 2*SnakeMain.panel_height)/12)*12)

        SnakeMain.foods = []
        for f in range(self.food_number):
            SnakeMain.foods.append(Food())

    def start(self):
        while True:
            SnakeMain.screen.fill((3, 3, 3))

            if len(SnakeMain.foods):
                for f in SnakeMain.foods:
                    if f:
                        f.display()
                        self.food = f
                        break
            else:
                self.game_over()

            SnakeMain.snake.display()
            if SnakeMain.snake.live:
                if not SnakeMain.stop:
                    SnakeMain.snake.move()
                    self.food.eaten()
            else:
                self.game_over()

            if len(SnakeMain.body):
                for b in SnakeMain.body:
                    b.display()
                if SnakeMain.snake.live and not SnakeMain.stop:
                    for i, b in enumerate(SnakeMain.body):
                        if not i:
                            b.move(SnakeMain.snake)
                        else:
                            b.move(SnakeMain.body[i-1])

            self.get_event()
            self.write_text()
            
            if SnakeMain.help:
                self.game_help()
                
            time.sleep(0.1)
            pygame.display.update()

    def write_text(self):
        subscreen = self.screen.subsurface((0, 0, SnakeMain.width, SnakeMain.panel_height))
        subscreen.fill((16, 16, 16))

        font = pygame.font.SysFont("arial", 18)
        color = (250, 250, 250)
        space = 5

        if SnakeMain.snake:
            mark = SnakeMain.snake.mark
        else:
            mark = 0

        text_mark = font.render("%s's mark : %d" % (SnakeMain.player["player"], mark), True, color)
        base_rect = text_mark.get_rect()
        base_rect.top = 5
        base_rect.left = 5
        SnakeMain.screen.blit(text_mark, base_rect)

        text_foods = font.render("food number : %s" % len(SnakeMain.foods), True, color)
        SnakeMain.screen.blit(text_foods, (base_rect.left, base_rect.top + base_rect.height + space))

        text_grade = font.render("player grade : %d"%SnakeMain.player['grade'], True, color)
        SnakeMain.screen.blit(text_grade, (SnakeMain.width - text_grade.get_rect().width - space, base_rect.top))

        help = font.render("help", True, (200, 200, 200))
        SnakeMain.help_rect["left"] = SnakeMain.width - help.get_rect().width - space
        SnakeMain.help_rect["top"] = base_rect.top + base_rect.height + space
        SnakeMain.help_rect["width"] = help.get_rect().width
        SnakeMain.help_rect["height"] = help.get_rect().height
        SnakeMain.screen.blit(help, (SnakeMain.help_rect["left"], SnakeMain.help_rect["top"]))

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit()
                
            if event.type == KEYDOWN:
                if SnakeMain.snake:
                    if event.key == K_LEFT or event.key == K_a:
                        SnakeMain.snake.direction = "L"
                    if event.key == K_RIGHT or event.key == K_d:
                        SnakeMain.snake.direction = "R"
                    if event.key == K_UP or event.key == K_w:
                        SnakeMain.snake.direction = "U"
                    if event.key == K_DOWN or event.key == K_s:
                        SnakeMain.snake.direction = "D"

                if event.key == K_ESCAPE:
                    self.exit()

                if event.key == K_r:
                    if not SnakeMain.snake.live:
                        self.restart()

                if event.key == K_n:
                    if SnakeMain.snake.live:
                        self.next()

                if event.key == K_SPACE:
                    if SnakeMain.stop:
                        SnakeMain.stop = False
                    else:
                        SnakeMain.stop = True
                        
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] <= (SnakeMain.help_rect["left"]+SnakeMain.help_rect["width"]) and pos[0] >= SnakeMain.help_rect["left"] and pos[1] >= SnakeMain.help_rect["top"] and pos[1] <= (SnakeMain.help_rect["top"]+SnakeMain.help_rect["height"]):
                    SnakeMain.help = True
                    SnakeMain.stop = True
                else:
                    SnakeMain.help = False
                    SnakeMain.stop = False

    def game_over(self):
        subscreen = self.screen.subsurface((SnakeMain.width/4, SnakeMain.height/4, SnakeMain.width/2, SnakeMain.height/2))
        subscreen.fill((14, 14, 55))

        font = pygame.font.SysFont("arial", 22)
        texts = []
        if not SnakeMain.snake.live and len(SnakeMain.foods):
            texts = [
                font.render("GAME OVER", True, (250, 250, 250)),
                font.render("press enter to restart game", True, (250, 50, 50))
            ]
        if not len(SnakeMain.foods) and SnakeMain.snake.live:
            SnakeMain.stop = True
            texts = [
                font.render("Congratulations!", True, (250, 250, 250)),
                font.render("press keyword n to next", True, (250, 50, 50))
            ]

        for s in texts:
            text_rect = s.get_rect()
            subscreen.blit(s, (SnakeMain.width / 4 - text_rect.width / 2, SnakeMain.height / 7 + 40 * texts.index(s), text_rect.width, text_rect.height))

    def restart(self):
        self.__init__(SnakeMain.player)
        self.start()

    def next(self):
        SnakeMain.player["grade"] += 1
        self.restart()

    def game_help(self):
        subscreen = self.screen.subsurface((SnakeMain.width/4, SnakeMain.height/4, SnakeMain.width/2, SnakeMain.height/2))
        subscreen.fill((40, 120, 30))

        font = pygame.font.SysFont("arial", 18)
        texts = [
            font.render("keyword up/w: change direction to up", True, (250, 250, 250)),
            font.render("keyword down/s: change direction to down", True, (250, 250, 250)),
            font.render("keyword left/a: change direction to left", True, (250, 250, 250)),
            font.render("keyword right/d: change direction to right", True, (250, 250, 250)),
            font.render("keyword space: to pause", True, (250, 250, 250)),
            font.render("keyword r: to restart", True, (250, 250, 250)),
            font.render("keyword n: to next", True, (250, 250, 250))
        ]

        for s in texts:
            text_rect = s.get_rect()
            subscreen.blit(s, (20, 15+30*texts.index(s), text_rect.width, text_rect.height))

    def exit(self):
        exit()

class BaseObj(pygame.sprite.Sprite):
    def __init__(self, left, top, color):
        pygame.sprite.Sprite.__init__(self)

        self.width = 12
        self.height = 12
        self.left = left
        self.top = top
        self.old_left = self.left
        self.old_top = self.top

    def display(self):
        pygame.draw.rect(SnakeMain.screen, self.color, (self.left, self.top, self.width, self.height))

class Snake(BaseObj):
    def __init__(self, left, top, color):
        super().__init__(left, top, color)

class Head(Snake):
    color = (255, 55, 55)
    def __init__(self, left, top):
        super().__init__(left, top, Head.color)
        self.direction = "U"
        self.mark = 0
        self.step = 12
        self.live = True

    def move(self):
        if not(self.left == SnakeMain.width-self.width or self.left == 0 or self.top == SnakeMain.panel_height or self.top == SnakeMain.height-self.height):
            self.old_left = self.left
            self.old_top = self.top

        if self.direction == "L":
            if self.left > 0:
                self.left -= self.step
            else:
                self.left = 0
                self.live = False

        if self.direction == "R":
            if self.left < SnakeMain.width-self.width:
                self.left += self.step
            else:
                self.left = SnakeMain.width-self.width
                self.live = False

        if self.direction == "U":
            if self.top > SnakeMain.panel_height:
                self.top -= self.step
            else:
                self.top = SnakeMain.panel_height
                self.live = False

        if self.direction == "D":
            if self.top < SnakeMain.height-self.height:
                self.top += self.step
            else:
                self.top = SnakeMain.height-self.height
                self.live = False

class Body(Snake):
    color = (255, 100, 100)

    def __init__(self, left, top):
        super().__init__(left, top, Body.color)

    def move(self, pre):

        if not (self.left == SnakeMain.width - self.width or self.left == 0 or self.top == SnakeMain.panel_height or self.top == SnakeMain.height - self.height):

            self.old_left = self.left
            self.old_top = self.top

            self.left = pre.old_left
            self.top = pre.old_top

class Food(BaseObj):
    color = (100, 255, 100)

    def __init__(self):
        self.top = 0
        self.left = 0
        self.width = 12
        self.height = 12
        self.get_rand_pos()
        super().__init__(self.left, self.top, Food.color)

    def get_rand_pos(self):
        while True:
            self.top = math.floor(randint(SnakeMain.panel_height, SnakeMain.height-self.height)/12)*12
            self.left = math.floor(randint(0, SnakeMain.width-self.width)/12)*12
            if self.top != SnakeMain.snake.top and self.left != SnakeMain.snake.left:
                break

    def eaten(self):
        if (SnakeMain.snake.left >= self.left and SnakeMain.snake.left <= self.left+self.width) and (SnakeMain.snake.top >= self.top and SnakeMain.snake.top <= self.top+self.height):
            if len(SnakeMain.foods):
                SnakeMain.foods.remove(self)
            SnakeMain.snake.mark += 100

            i = len(SnakeMain.body)
            if i:
                l = SnakeMain.body[i-1].old_left
                t = SnakeMain.body[i-1].old_top
            else:
                l = SnakeMain.snake.old_left
                t = SnakeMain.snake.old_top
            SnakeMain.body.append(Body(l, t))

if __name__ == "__main__":
    game = SnakeMain()
    game.start()
