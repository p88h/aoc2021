import pygame
from common import View, Controller
from pygame import gfxdraw as gd


class Point:
    def __init__(self, pos):
        self.pos = pos
        self.target = pos
        self.sx = 1
        self.sy = 1
        self.ms = 1
        self.maxs = 1

    def update(self, view, base):
        (x, y) = self.pos
        (bx, by) = base
        if self.pos != self.target:
            (tx, ty) = self.target
            if self.ms > abs(x - tx) + abs(y - ty):
                self.ms = abs(x - tx) + abs(y - ty)
            if x != tx:
                x += self.ms if x < tx else -self.ms
            if y != ty:
                y += self.ms if y < ty else -self.ms
            if self.ms < self.maxs:
                self.ms += 1
            self.pos = (x, y)
        else:
            self.ms = 1
        if self.sx == 1 and self.sy == 1:
            gd.pixel(view.win, x + bx, y + by, (255, 255, 255))
        else:
            pygame.draw.rect(view.win, (255, 255, 255),
                             (bx+x*self.sx, by+y*self.sy, self.sx, self.sy))


class Space:
    def __init__(self, points, pos=(0, 0)):
        self.pos = pos
        self.points = points
        self.divider = None
        self.folds = []

    def update(self, view, controller):
        for p in self.points:
            p.update(view, self.pos)
        for f in self.folds:
            f.update(view, controller)
        if self.divider:
            (dx, dy) = self.divider
            (x, y) = self.pos
            if x == 64 and dy > 0:
                pygame.draw.line(view.win, (120, 120, 120), (0, y + dy), (1440, y + dy))
            if y == 34 and dx > 0:
                pygame.draw.line(view.win, (120, 120, 120), (x + dx, 0), (x + dx, 960))

    def fold(self, pos):
        (x, y) = pos
        if self.folds:
            self.folds[0].fold(pos)
            self.folds[1].fold(pos)
            return
        (a, b) = ([], [])
        maxs = (x + y) // 20
        for p in self.points:
            (px, py) = p.target
            if x > 0 and px > x:
                p.pos = (px - x, py)
                px = x - abs(px - x)
                p.target = (px, py)
                p.maxs = maxs
                b.append(p)
            elif y > 0 and py > y:
                p.pos = (px, py - y)
                py = y - abs(py - y)
                p.target = (px, py)
                p.maxs = maxs
                b.append(p)
            else:
                a.append(p)
        (sx, sy) = self.pos
        if x > 0:
            x += 1
        else:
            y += 1
        self.folds = [Space(a, self.pos), Space(b, (x + sx, y + sy))]
        self.points = []
        self.divider = pos

    def collapse(self):
        if self.folds[0].folds:
            self.folds[0].collapse()
            self.folds[1].collapse()
        else:
            (dx, dy) = self.divider
            sx = 2 if dx > 0 else 1
            sy = 2 if dy > 0 else 1
            self.points = []
            for p in self.folds[0].points:
                (px, py) = p.pos
                p.sx *= sx
                p.sy *= sy
                px //= sx
                py //= sy
                p.pos = (px, py)
                p.maxs = 2 if dx > 0 else 1
                self.points.append(p)
            for p in self.folds[1].points:
                (px, py) = p.pos
                p.sx *= sx
                p.sy *= sy
                px = px // sx + dx // p.sx
                py = py // sy + dy // p.sy
                p.pos = (px, py)
                p.maxs = 2 if dx > 0 else 1
                self.points.append(p)
            self.divider = None
            self.folds = []


class Splitter:
    def __init__(self, space, splits):
        self.space = space
        self.splits = splits
        self.si = 0

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0, 0, 0))
        self.space.update(view, controller)
        if view.frame % 30 == 0 and self.si < len(self.splits):
            self.space.fold(self.splits[self.si])
            self.si += 1
        elif view.frame % 30 == 0 and self.space.folds:
            self.space.collapse()


def init(controller):
    points = []
    splits = []
    maxx = 0
    maxy = 0
    with open(controller.workdir() + "/input/day13.txt") as f:
        for l in f.read().splitlines():
            if ',' in l:
                (x, y) = tuple(map(int, l.split(",")))
                points.append(Point((x, y)))
                maxx = max(x, maxx)
                maxy = max(y, maxy)
            if 'x=' in l:
                splits.append((int(l.split('=')[1]), 0))
            if 'y=' in l:
                splits.append((0, int(l.split('=')[1])))
        controller.add(Splitter(Space(points, (64, 34)), splits))
    return controller


view = View(1440, 960, 30)
view.setup("Day 13")
controller = Controller()
init(controller).run(view)
