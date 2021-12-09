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
        self.color = (100,random.randint(100,240),random.randint(100,240),100)

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent
    
    def union(self, other):
        a = self.find()
        b = other.find()
        if a != b:
            a.parent = b

    def update(self, view, level):
        (x, y) = self.pos
        y0 = y - self.height
        y1 = y + (self.height // 2)
        
        col1 = (160,160,160)
        col2 = (255,255,255)
        pygame.draw.polygon(view.win, col1, [(x,y0),(x+8,y0-4),(x+16,y0),(x+8,y0+4)])
        pygame.draw.polygon(view.win, col2, [(x,y0),(x+8,y0-4),(x+16,y0),(x+8,y0+4)],1)
        col3 = (80,80,80)
        col4 = (40,40,40)
        pygame.draw.polygon(view.win, col4, [(x,y0),(x+8,y0+4),(x+16,y0),
                                             (x+16,y1),(x+8,y1+4),(x,y1)])
        pygame.draw.line(view.win, col3, (x,y0), (x,y1))
        pygame.draw.line(view.win, col3, (x+8,y0+4), (x+8,y1+4))
        pygame.draw.line(view.win, col3, (x+16,y0), (x+16,y1))

        if int(level) > self.height:
            yw = y - int(level) + random.randint(-1,1)
            pygame.draw.polygon(view.win, self.find().color, [(x,yw),(x+9,yw-5),(x+18,yw),(x+9, yw+5)])

class Water:
    def __init__(self):
        self.surf = pygame.Surface((1920,1080), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        self.level = 0.0
        self.board = []
        pass

    def update(self, view, controller):
        view.win.fill((0,0,0,0))
        self.surf.fill((0,0,0,0))
        if self.level < 17:
            self.level += 0.1
        else:
            controller.animate = False
        h = len(self.board)
        for y in range(h):
            w = len(self.board[y])
            for x in range(w):
                tile = self.board[y][x]
                if tile.height < int(self.level) and not tile.covered:
                    if x > 0 and self.board[y][x-1].covered:
                        tile.union(self.board[y][x-1])
                    if y > 0 and self.board[y-1][x].covered:
                        tile.union(self.board[y-1][x])
                    if x < w - 1 and self.board[y][x+1].covered:
                        tile.union(self.board[y][x+1])
                    if y < h - 1 and self.board[y+1][x].covered:
                        tile.union(self.board[y+1][x])
                    tile.covered = True
                tile.update(view, self.level)
        view.win.blit(self.surf, (0,0))

def init(my_dir, controller):
    water = Water()
    with open(my_dir + "/input/day09.txt") as f:
        y = 0
        for l in f.read().splitlines():
            w = len(l)-1
            line = [ Tile(w-x, y, int(l[w-x])) for x in range(len(l)) ]
            water.board.append(line)
            y += 1
    controller.add(water)        

view = View(1920,1080,30)
view.setup("Day 09")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
init(my_dir, controller)
view.record(my_dir + "/day9.mp4")
controller.run(view)
