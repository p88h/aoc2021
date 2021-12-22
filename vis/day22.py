import itertools
import pygame
import re
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

class Plotter:
    def __init__(self, lines):
        self.pos = (0, 0)
        self.boxes = []
        self.dims = []
        self.tiles = []
        self.voxels = [ 0 ] * (100*100*100)
        self.tile = Tile(8)
        for line in lines:
            m = re.search(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', line)
            x0,x1,y0,y1,z0,z1 = [(int(m.group(i))+100000)//2000 for i in range(2,8)]
            bit = 1 if m.group(1) == "on" else 0
            self.dims.append(([(x0,x1+1),(y0,y1+1),(z0,z1+1)], bit))            

    def update(self, view, controller):
        if view.frame >= len(self.dims) - 1:
            controller.animate = False
        if not controller.animate:
            return
        view.win.fill((0,0,0))
        idx = view.frame
        (seq, val) = self.dims[idx]
        print("Adding box ", seq)
        [(x0,x1),(y0,y1),(z0,z1)] = seq
        for (x,y,z) in itertools.product(range(x0,x1),range(y0,y1),range(z0,z1)):
            self.voxels[z*100*100+y*100+x] = val
        for (z,y,x) in itertools.product(range(0,100),range(0,100),range(99,-1,-1)):
            # pos = (20 + x * 5 + y * 5, 642 - x * 3 + y * 3 - z*4)
            pos = (60 + x * 9 + y * 9, 972 - x * 5 + y * 5 - z * 8)
            if self.voxels[z*100*100+y*100+x]:
                self.tile.blit(view.win, pos)
        

def init(controller):
    with open(controller.workdir() + "/input/day22.txt") as f:
        controller.add(Plotter(f.read().splitlines()))
    return controller

view = View(1920,1200,6)
view.setup("Day 22")
controller = Controller()
init(controller).run(view)
