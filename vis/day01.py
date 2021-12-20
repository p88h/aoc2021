import pygame
import math
from common import View, Controller


class Background:
    def __init__(self, base_path, view, scale=10):
        self.blocks = view.width // scale
        self.center = 2 * view.height // 3
        self.scale = scale
        with open(base_path + "/input/day01.txt") as f:
            self.hmap = list(map(int, f.read().splitlines()))
            self.base = max(self.hmap[0: self.blocks // 2])

    def update(self, view, controller):
        if view.frame >= len(self.hmap) - self.blocks:
            controller.animate = False

        view.win.fill((0, 0, 0))
        ofs = view.frame
        base1 = max(self.hmap[ofs:ofs + self.blocks // 2])
        if base1 > self.base + 6:
            base1 = self.base + 6
        if base1 < self.base:
            base1 = self.base
        self.base = base1
        for idx in range(1, self.blocks):
            x0 = self.scale * (idx-1)
            y0 = self.center - (self.base - self.hmap[ofs+idx-1])
            x1 = self.scale * idx
            y1 = self.center - (self.base - self.hmap[ofs+idx])
            color = (140, 140, 140)
            width = 1
            if y1 > y0 and idx > 20 and idx < 80:
                color = (160, 255, 160)
                width = 2
            pygame.draw.line(view.win, color, (x0, y0), (x1, y1), width)


class UBoot:
    def __init__(self, bg):
        self.background = bg
        self.hover = bg.base - bg.hmap[10]
        pass

    def update(self, view, _):
        ofs = view.frame
        hover1 = self.background.base - self.background.hmap[ofs+10]
        if hover1 > self.hover + 8:
            self.hover += 2
        if hover1 < self.hover - 8:
            self.hover -= 2

        h = self.background.center - self.hover - 200
        PI = math.pi

        pygame.draw.arc(view.win, (240, 180, 180), [120, h-20, 40, 20], 0, 2*PI, 2)
        for l in range(4):
            dim = 5*((ofs+16-l*4) % 16)
            pygame.draw.arc(view.win, (180-dim, 240-dim, 240-dim),
                            [124+l*8, h-12, 5, 5], 0, 2*PI, 4)
        for r in range(16):
            b = r*r+(ofs % 16)
            pygame.draw.arc(view.win, (160-r*10, 255-r*10, 160-r*10), [160, h, b, b], 3*PI/2, 2*PI)


view = View()
view.setup("Day 01")
controller = Controller()
bg = Background(controller.workdir(), view)
controller.add(bg)
controller.add(UBoot(bg))
controller.run(view)
