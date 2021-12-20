import pygame
import heapq
import itertools
from common import View, Controller


class Tile:
    def __init__(self, x, y, h):
        self.pos = (40 + x * 9 + y * 9, 572 - x * 5 + y * 5)
        self.cost = h
        self.parent = self
        self.distance = 999999999
        self.done = False
        self.selected = False
        self.prev = None
        self.update_block()

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

    def update_block(self):
        if self.done:
            self.height = self.distance // 2
            self.color = (120, 120, 250) if self.selected else (120, 250, 120)
        elif self.distance < 999999999:
            self.color = (220, 120, 80)
        else:
            self.color = (160, 160, 160)
            self.height = self.cost * 2
        self.tmp = pygame.Surface((16, self.height + 8), pygame.SRCALPHA)
        self.tmp.fill((0, 0, 0, 0))
        self.render(self.tmp, (0, 4))

    def render_block(self, surface, ofs):
        (x, y) = self.pos
        if self.done:
            y += ofs
        surface.blit(self.tmp, (x, y - self.height))


class Board:
    def __init__(self, tiles):
        self.tiles = tiles
        self.tiles[0][0].distance = 0
        self.pq = [(0, (0, 0))]
        self.rn = list(range(len(self.tiles)))
        self.rn.reverse()
        self.maxs = 0
        self.maxh = 0
        self.path = []
        heapq.heapify(self.pq)

    def bfsstep(self):
        st = None
        while not st and self.pq:
            (v, (y, x)) = heapq.heappop(self.pq)
            st = self.tiles[y][x]
            if st.done:
                st = None
        if not st:
            return False
        st.done = True
        st.update_block()
        if st.height > self.maxh:
            self.maxh = st.height
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if y + dy >= 0 and y + dy < 100 and x + dx >= 0 and x + dx < 100:
                dt = self.tiles[y + dy][x + dx]
                nd = v + dt.cost
                if nd < dt.distance:
                    dt.distance = nd
                    dt.prev = st
                    dt.update_block()
                    heapq.heappush(self.pq, (nd, (y + dy, x + dx)))
        return True

    def update(self, view, controller):
        if not self.bfsstep():
            controller.animate = False
        if not controller.animate:
            return
        for i in range(self.maxs):
            self.bfsstep()
        if self.maxs < 4:
            self.maxs += 1

        for t in self.path:
            t.selected = False
        npath = []
        for i in self.rn:
            st = self.tiles[i][i]
            if st.done:
                while st.prev:
                    npath.append(st)
                    st.selected = True
                    st.update_block()
                    st = st.prev
                break
        for t in self.path:
            if not t.selected:
                t.update_block()
        self.path = npath

        view.win.fill((0, 0, 0, 0))
        for (y, x) in itertools.product(self.rn, self.rn):
            self.tiles[y][x].render_block(view.win, self.maxh)


def init(controller):
    board = []
    with open(controller.workdir() + "/input/day15.txt") as f:
        y = 0
        for l in f.read().splitlines():
            w = len(l) - 1
            line = [Tile(x, w - y, int(l[x])) for x in range(len(l))]
            board.append(line)
            y += 1
    controller.add(Board(board))
    return controller


view = View(1920, 1080, 30)
view.setup("Day 15")
init(Controller()).run(view)
