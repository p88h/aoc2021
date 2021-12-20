import pygame
from common import View, Controller


class Background:
    def __init__(self, base_path):
        self.pos = (0, 0)
        with open(base_path + "/input/day02.txt") as f:
            self.lines = f.read().splitlines()

    def update(self, view, controller):
        if view.frame >= len(self.lines) - 1:
            controller.animate = False
        if not controller.animate:
            return

        idx = view.frame
        l = self.lines[idx].split()
        v = int(l[1])
        (x0, y0) = self.pos
        (x1, y1) = self.pos
        if l[0] == "forward":
            x1 += v
        if l[0] == "down":
            y1 += v
        if l[0] == "up":
            y1 -= v
        pygame.draw.line(view.win, (180, 180, 240), (x0, y0), (x1, y1), 2)
        self.pos = (x1, y1)


view = View()
view.setup("Day 02")
controller = Controller()
controller.add(Background(controller.workdir()))
controller.run(view)
