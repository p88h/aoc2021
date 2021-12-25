import pygame
from common import View, Controller

class Tile:
    def __init__(self, height, color, chr = None):
        self.height = height
        self.color = color
        self.chr = chr
        self.size = 3
        self.tmp = pygame.Surface((16, self.height + 8), pygame.SRCALPHA)
        self.tmp.fill((0, 0, 0, 0))
        self.render(self.tmp, (0, 4))

    def render(self, surface, pos):
        (x, y0) = pos
        y1 = y0 + self.height
        B = self.size

        col2 = (255, 255, 255)
        pygame.draw.polygon(surface, self.color, [(x, y0), (x + B*2, y0 - B), (x + B*4, y0),
                                                  (x + B*2, y0 + B)])
        pygame.draw.polygon(surface, col2, [(x, y0), (x + B*2, y0 - B), (x + B*4, y0),
                                            (x + B*2, y0 + B)], 1)
        col3 = (80, 80, 80)
        col4 = (40, 40, 40)
        #if self.chr == '>':
        #    pygame.draw.line(surface,col3,(x+6,y0+2),(x+10,y0-2))
        #elif self.chr == 'v':
        #    pygame.draw.line(surface,col3,(x+8,y0-2),(x+8,y0+2))
        pygame.draw.polygon(surface, col4, [(x, y0), (x + B*2, y0 + B), (x + B*4, y0), (x + B*4, y1),
                                            (x + B*2, y1 + B), (x, y1)])
        pygame.draw.line(surface, col3, (x, y0), (x, y1))
        pygame.draw.line(surface, col3, (x + B*2, y0 + B), (x + B*2, y1 + B))
        pygame.draw.line(surface, col3, (x + B*4, y0), (x + B*4, y1))

    def blit(self, surface, pos):
        (x, y) = pos
        surface.blit(self.tmp, (x, y - self.height))

class Plotter:
    def __init__(self, lines):
        self.pos = (0, 0)
        self.boxes = []
        self.dims = []
        self.h = len(lines)
        self.w = len(lines[0])
        self.tiles = { '.': Tile(0, (160,160,220)), 
                       'v': Tile(8, (220,160,160), 'v'),
                       '>': Tile(8, (160,220,160), '>') }
        self.lines = lines
        self.mc = 0

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0,0,0))
        if view.frame % 2 == 1:
            dx, dy, dc = 0, 1, 'v'
        else:
            dx, dy, dc = 1, 0, '>'
            self.mc = 0
        newlines = []
        for y in range(0,self.h):
            newlines.append(list(self.lines[y]))
        for y in range(0,self.h):
            ny = (y+dy)%self.h
            for x in range(0,self.w):
                nx = (x+dx)%self.w
                if self.lines[y][x] == dc and self.lines[ny][nx] == '.':
                    newlines[ny][nx] = dc
                    newlines[y][x] = '.'
                    self.mc += 1
        print(dc,dx,dy, view.frame//2, self.mc)
        for y in range(0,self.h):
            self.lines[y]="".join(newlines[y])
            for x in range(0,self.w)[::-1]:
                ch = self.lines[y][x]
                pos = (10 + x * 7 + y * 7, 540 - x * 4 + y * 4)
                self.tiles[ch].blit(view.win, pos)
        txt = "Move: {} {}".format(view.frame//2+1, dc)
        view.font.render_to(view.win, (20, 20), txt, (255, 255, 255))
        if self.mc == 0 and dc =='v':
            controller.animate = False
        

def init(controller):
    with open(controller.workdir() + "/input/day25.txt") as f:
        controller.add(Plotter(f.read().splitlines()))
    return controller

view = View(1920,1080,8)
view.setup("Day 25")
controller = Controller()
init(controller).run(view)
