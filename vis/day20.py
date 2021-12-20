import pygame
import itertools
from common import View, Controller


class Tile:
    def __init__(self, height):
        self.height = height
        self.color = (200,200,200) if height>0 else (160, 160, 160)
        self.tmp = pygame.Surface((16, self.height + 8), pygame.SRCALPHA)
        self.tmp.fill((0, 0, 0, 0))
        self.render(self.tmp, (0, 4))

    def render(self, surface, pos):
        (x, y0) = pos
        y1 = y0 + self.height

        col2 = (255, 255, 255)
        pygame.draw.polygon(surface, self.color, [(x, y0), (x + 8, y0 - 4), (x + 16, y0),
                                                  (x + 8, y0 + 4)])
        pygame.draw.polygon(surface, col2, [(x, y0), (x + 8, y0 - 4), (x + 16, y0),
                                            (x + 8, y0 + 4)], 1)
        col3 = (80, 80, 80)
        col4 = (40, 40, 40)
        pygame.draw.polygon(surface, col4, [(x, y0), (x + 8, y0 + 4), (x + 16, y0), (x + 16, y1),
                                            (x + 8, y1 + 4), (x, y1)])
        pygame.draw.line(surface, col3, (x, y0), (x, y1))
        pygame.draw.line(surface, col3, (x + 8, y0 + 4), (x + 8, y1 + 4))
        pygame.draw.line(surface, col3, (x + 16, y0), (x + 16, y1))

    def blit(self, surface, pos):
        (x, y) = pos
        surface.blit(self.tmp, (x, y - self.height))


class Board:
    def __init__(self, rules, lines):
        self.tiles = [Tile(0), Tile(8)]
        self.minx = self.miny = self.maxx = 0
        self.bitmap = [ 1 if c == '#' else 0 for c in rules ]
        self.maxy = len(lines)
        self.board = {}
        self.dflt = 0
        for y in range(len(lines)):
            self.maxx = max(self.maxx, len(lines[y]))
            for x in range(len(lines[y])):
                self.board[(x, y)] = 1 if lines[y][x] == '#' else 0
        self.ofsx = (100-self.maxx)//2
        self.ofsy = (100-self.maxy)//2

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0, 0, 0, 0))
        for (x, y) in itertools.product(range(self.minx, self.maxx), range(self.miny, self.maxy)):
            if (x, y) in self.board:
                rx = 99-(x+self.ofsx)
                ry = y+self.ofsy
                pos = (60 + rx * 9 + ry * 9, 572 - rx * 5 + ry * 5)
                if self.board[(x, y)]:
                    self.tiles[1].blit(view.win, pos)
        # new default value for tiles outside of the board
        ndflt = self.bitmap[0] if self.dflt == 0 else self.bitmap[-1]
        self.minx -= 1
        self.miny -= 1
        self.maxx += 1
        self.maxy += 1
        total = 0
        old = self.board.copy()
        for (x, y) in itertools.product(range(self.minx, self.maxx), range(self.miny, self.maxy)):
            fval = 0
            for (dx,dy) in [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]:
                bit = old.get((x+dx,y+dy), self.dflt)
                fval = fval * 2 + bit
            nbit = self.bitmap[fval]
            total += nbit
            # skip inserting unnecesary pixels. 
            # This looks better but might not be always corect
            if (x,y) not in self.board and (fval==0 or fval==511):
               continue
            self.board[(x,y)]=nbit
        self.dflt = ndflt
        print(view.frame + 1, total, ndflt)


def init(controller):
    with open(controller.workdir() + "/input/day20.txt") as f:
        lines = f.read().splitlines()
        controller.add(Board(lines[0], lines[2:]))
    return controller


view = View(1920, 1080, 6)
view.setup("Day 20")
init(Controller()).run(view)
