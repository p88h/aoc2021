import pygame
from common import View, Controller


class Tile:
    def __init__(self, x, y, h):
        self.loc = (y, x)
        self.pos = (x * 18 + y * 18, 240 - x * 10 + y * 10)
        self.level = h
        self.flashing = False

    def render(self, surface):
        (x, y) = self.pos
        y0 = y - self.level

        col1 = (160, 255, 160) if self.flashing else (160, 160, 200)
        col2 = (255, 255, 255)
        pygame.draw.polygon(surface, col1, [(x, y0), (x+16, y0-8), (x+32, y0), (x+16, y0+8)])
        pygame.draw.polygon(surface, col2, [(x, y0), (x+16, y0-8), (x+32, y0), (x+16, y0+8)], 1)
        col3 = (80, 80, 80)
        col4 = (40, 40, 40)
        pygame.draw.polygon(surface, col4, [(x, y0), (x+16, y0+8), (x+32, y0),
                                            (x+32, y), (x+16, y+8), (x, y)])
        pygame.draw.line(surface, col3, (x, y0), (x, y))
        pygame.draw.line(surface, col3, (x+16, y0+8), (x+16, y+8))
        pygame.draw.line(surface, col3, (x+32, y0), (x+32, y))

    def increase(self, amount):
        if not self.flashing:
            if self.level + amount >= 30:
                self.level = 30
                self.flashing = True
                return [self]
            else:
                self.level += amount
        return []

    def propagate(self, board):
        (ti, tj) = self.loc
        flashed = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if ti + i >= 0 and ti + i < len(board) and tj + j >= 0 and tj + j < len(board[i]):
                    flashed.extend(board[ti + i][tj + j].increase(3))
        return flashed


class Game:
    def __init__(self, board):
        self.board = board
        self.flashing = []

    def update(self, view, controller):
        if not controller.animate:
            return
        view.win.fill((0, 0, 0))

        fcnt = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                tile = self.board[y][x]
                if tile.flashing:
                    tile.level //= 2
                    fcnt += 1

        if self.flashing:
            nextflash = []
            for tile in self.flashing:
                nextflash.extend(tile.propagate(self.board))
            self.flashing = nextflash
            fcnt += len(nextflash)

        for y in range(len(self.board)):
            w = len(self.board[y])
            for xr in range(w):
                tile = self.board[y][w - xr - 1]
                if fcnt == 0:
                    self.flashing.extend(tile.increase(1))
                elif not self.flashing and tile.flashing:
                    tile.flashing = False
                    tile.level = 0
                tile.render(view.win)

        if len(self.flashing) == 400:
            controller.animate = False


def init(controller):
    board = []
    with open(controller.workdir() + "/input/day11.txt") as f:
        y = 0
        lines = f.read().splitlines()
        for _r in range(2):
            for l in lines:
                line = [Tile(x, y, 3 * int(l[x])) for x in range(len(l))]
                lx = len(line)
                line.extend([Tile(x+lx , y, 3 * int(l[x])) for x in range(len(l))])
                board.append(line)
                y += 1
    controller.add(Game(board))
    return controller


view = View(720, 480, 50)
view.setup("Day 11")
controller = Controller()
init(controller).run(view)
