# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pygame
import os
import random
from common import View, Controller
from functools import reduce

class Tile:
    def __init__(self, x, y, h):
        self.pos = (40+ x*9+y*9, 540-x*5+y*5)
        self.height = h * 2
        self.parent = self
        self.covered = False
        self.color = (100,random.randint(100,240),random.randint(100,240),160)
        self.done = False

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent
    
    def union(self, other):
        a = self.find()
        b = other.find()
        if a != b:
            a.parent = b

    def render_block(self, surface):
        (x, y) = self.pos
        y0 = y - self.height

        col1 = (160,160,160)
        col2 = (255,255,255)
        pygame.draw.polygon(surface, col1, [(x,y0),(x+8,y0-4),(x+16,y0),(x+8,y0+4)])
        pygame.draw.polygon(surface, col2, [(x,y0),(x+8,y0-4),(x+16,y0),(x+8,y0+4)],1)
        col3 = (80,80,80)
        col4 = (40,40,40)
        pygame.draw.polygon(surface, col4, [(x,y0),(x+8,y0+4),(x+16,y0),
                                             (x+16,y),(x+8,y+4),(x,y)])
        pygame.draw.line(surface, col3, (x,y0), (x,y))
        pygame.draw.line(surface, col3, (x+8,y0+4), (x+8,y+4))
        pygame.draw.line(surface, col3, (x+16,y0), (x+16,y))

    def render_water(self, surface, level):
        (x, y) = self.pos
        if int(level) > self.height:
            (r,g,b,a) = self.find().color
            yw = y - int(level) + random.randint(-1,1)
            pygame.draw.polygon(surface, (r,g,b,a), [(x,yw),(x+8,yw-4),(x+16,yw),(x+8, yw+4)])
            pygame.draw.polygon(surface, (r,g,b,a + 40), [(x-1,yw),(x+8,yw-5),(x+17,yw),(x+8, yw+5)],1)
            self.covered = True


class Background:
    def __init__(self, board):
        self.surf = pygame.Surface((1920,1080))
        self.surf.fill((0,0,0,0))
        for y in range(len(board)):
            for x in range(len(board[y])):
                board[y][x].render_block(self.surf)

    def update(self, view, _):
        view.win.fill((0,0,0,0))
        view.win.blit(self.surf, (0,0))


class Water:
    def __init__(self, board):
        self.surf = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.level = 0.0
        self.board = board

    def update(self, view, controller):
        self.surf.fill((0,0,0,0))
        merge = 0
        if self.level < 17:
            self.level += 0.1
        else:
            merge = 10
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                tile = self.board[y][x]
                if merge > 0 and tile.covered and not tile.done:
                    if x > 0 and self.board[y][x-1].covered:
                        tile.union(self.board[y][x-1])
                    if y > 0 and self.board[y-1][x].covered:
                        tile.union(self.board[y-1][x])
                    tile.done = True
                    merge -= 1
                tile.render_water(self.surf, self.level)
        view.win.blit(self.surf, (0,0))
        if merge > 0:
            controller.animate = False

def init(my_dir, controller):
    board = []
    with open(my_dir + "/input/day09.txt") as f:
        y = 0
        for l in f.read().splitlines():
            w = len(l)-1
            line = [ Tile(w-x, y, int(l[w-x])) for x in range(len(l)) ]
            board.append(line)
            y += 1
    controller.add(Background(board))
    controller.add(Water(board))

view = View(1920,1080,60)
view.setup("Day 09")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
init(my_dir, controller)
view.record(my_dir + "/day9.mp4")
controller.run(view)
