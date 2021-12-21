import pygame
import itertools
import math
from collections import defaultdict
from common import View, Controller


class Tile:
    def __init__(self, height):
        self.height = height
        self.color = (200, 200, 200)
        self.tmp = pygame.Surface((8, self.height + 4), pygame.SRCALPHA)
        self.tmp.fill((0, 0, 0, 0))
        self.render(self.tmp, (0, 2))

    def render(self, surface, pos):
        (x, y0) = pos
        y1 = y0 + self.height

        col2 = (255, 255, 255)
        pygame.draw.polygon(surface, self.color, [(x, y0), (x + 4, y0 - 2), (x + 8, y0),
                                                  (x + 4, y0 + 2)])
        pygame.draw.polygon(surface, col2, [(x, y0), (x + 4, y0 - 2), (x + 8, y0),
                                            (x + 4, y0 + 2)], 1)
        col3 = (80, 80, 80)
        col4 = (40, 40, 40)
        pygame.draw.polygon(surface, col4, [(x, y0), (x + 4, y0 + 2), (x + 8, y0), (x + 8, y1),
                                            (x + 4, y1 + 2), (x, y1)])
        pygame.draw.line(surface, col3, (x, y0), (x, y1))
        pygame.draw.line(surface, col3, (x + 4, y0 + 2), (x + 4, y1 + 2))
        pygame.draw.line(surface, col3, (x + 8, y0), (x + 8, y1))

    def blit(self, surface, pos):
        (x, y) = pos
        surface.blit(self.tmp, (x, y - self.height))


class Board:
    def __init__(self, pos):
        self.tiles = [Tile(h) for h in range(128)]
        self.multiverse = defaultdict(int)
        self.multiverse[(pos[0], pos[1], 0, 0)] = 1
        self.wins = [0, 0]
        self.player = 0
        self.steps = 0

    def produce3(self, p1, p2, s1, s2, c, w, p):
        if c == 0:
            return
        self.steps += 1
        for (d, f) in [(6, 7), (5, 6), (7, 6), (4, 3), (8, 3), (3, 1), (9, 1)]:
            np = ((p1 + d - 1) % 10) + 1
            ns = s1 + np
            if ns < 21:
                self.multiverse[(p2, np, s2, ns)] += c*f
            else:
                w[p] += c*f

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0, 0, 0, 0))
        total = 0
        for (s1, p1) in itertools.product(range(0, 21), range(1, 11)):
            for (s2, p2) in itertools.product(range(0, 21), range(1, 11)):
                x = 209 - (s1 * 10 + p1 - 1)
                y = 209 - (s2 * 10 + p2 - 1)
                key = (p1, p2, s1, s2) if self.player == 0 else (p2, p1, s2, s1)
                total += self.multiverse[key]
                if self.multiverse[key] > 0:
                    h = int(1+math.log2(self.multiverse[key]))
                else:
                    h = 0
                pos = (20 + x * 5 + y * 5, 642 - x * 3 + y * 3)
                self.tiles[h].blit(view.win, pos)
        if total > 0:
            old = self.multiverse.copy()
            self.multiverse = defaultdict(int)
            for (p1, p2, s1, s2) in old:
                self.produce3(p1, p2, s1, s2, old[(p1, p2, s1, s2)], self.wins, self.player)
            self.player = 1-self.player
        text = ["Player 1 wins: {}".format(self.wins[0]),
                "Player 2 wins: {}".format(self.wins[1]),
                "Quantum multiverse count: {}".format(total),
                "Dice rolls considered: {}".format(self.steps)]
        for it in range(len(text)):
            view.font.render_to(view.win, (20, (it+1)* 20 ), text[it], (255, 255, 255))


def init(controller):
    with open(controller.workdir() + "/input/day21.txt") as f:
        lines = f.read().splitlines()
        pos = [int(l.split(": ")[1]) for l in lines]
        controller.add(Board(pos))
    return controller


view = View(2144, 1280, 1)
view.setup("Day 21")
init(Controller()).run(view)
