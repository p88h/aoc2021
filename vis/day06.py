import pygame
import random
from common import View, Controller


class Background:
    def __init__(self):
        pass

    def update(self, view, controller):
        if view.frame == 800:
            controller.animate = False
        if not controller.animate:
            return
        text = "Day: {} Fish: {}".format(view.frame // 10, len(controller.objects) - 1)
        view.win.fill((0, 0, 0))
        view.font.render_to(view.win, (10, 16), text, (255, 255, 255))


def rndmod(value, factor, limit):
    (a, b) = limit
    value += random.randint(-factor, factor)
    value = max(a, value)
    value = min(b, value)
    return value


def posmod(view, pos, factor=0):
    (x, y) = pos
    x = rndmod(x, factor, (5, view.width-5))
    y = rndmod(y, factor, (40, view.height-5))
    return (x, y)


class Fish:
    def __init__(self, counter, pos=None, col=None):
        self.pos = pos
        self.col = col if col else (random.randint(160, 255),
                                    random.randint(160, 255),
                                    random.randint(160, 255))
        self.counter = counter

    def update(self, view, controller):
        if not controller.animate:
            return
        if not self.pos:
            self.pos = (random.randint(5, view.width), random.randint(5, view.height))
        (x, y) = posmod(view, self.pos, 2)
        if view.frame % 10 == 9:
            if self.counter == 0:
                self.counter = 6
                dx = random.randint(-3, 3)
                dy = random.randint(-3, 3)
                (r, g, b) = self.col
                ncol = (rndmod(r, 5, (0, 255)), rndmod(g, 5, (0, 255)), rndmod(b, 5, (0, 255)))
                controller.add(Fish(9, (x + dx, y + dy), ncol))
                x -= dx
                y -= dy
            else:
                self.counter -= 1

        mass = 9 - self.counter

        pygame.draw.circle(view.win, self.col, (x, y), mass, 2)
        if (mass > 2):
            pygame.draw.line(view.win, self.col, (x-mass-4, y-4), (x-mass-4, y+4), 2)
            pygame.draw.line(view.win, self.col, (x-mass-4, y-4), (x-mass, y), 2)
            pygame.draw.line(view.win, self.col, (x-mass-4, y+4), (x-mass, y), 2)
        if (mass > 5):
            pygame.draw.line(view.win, self.col, (x+mass/2, y-1), (x+mass/2+2, y-1), 2)
        self.pos = (x, y)


def init(controller):
    controller.add(Background())
    with open(controller.workdir() + "/input/day06.txt") as f:
        for f in map(int, f.readline().split(",")):
            controller.add(Fish(f))
    return controller


view = View(1920, 1080, 15)
view.setup("Day 02")
controller = Controller()
init(controller).run(view)
