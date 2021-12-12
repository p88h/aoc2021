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
import math
from common import View, Controller
from functools import reduce

class Cave:
    def __init__(self, name, font):
        self.pos = (random.randint(0,1920), random.randint(0,1080))
        self.name = name
        radius = 32 if name[0] >= "A" and name[0] <= "Z" else 16
        PI = math.pi
        points = [(radius*2 + math.cos(2*PI/32*x)*radius*2 + random.randint(0,4),
                   radius + math.sin(2*PI/32*x)*radius + random.randint(0,4)) for x in range(33)]
        self.surf = pygame.Surface((radius * 4 + 4, radius * 2+ 4), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        col2 = (160,255,220)
        col1 = (140,140,80)
        pygame.draw.polygon(self.surf, col1, points)
        pygame.draw.polygon(self.surf, col2, points, 1)
        font.render_to(self.surf, (radius * 2 - len(name)*4, radius+4), self.name, (0, 0, 0))
        self.clicked = False
        self.size = radius * 2

    def click(self, pos, press):
        if self.clicked and not press:
            self.pos = pygame.mouse.get_pos()
            self.clicked = False
        if press:
            (x, y) = self.pos
            (mx, my) = pos
            self.clicked = math.sqrt(math.pow(mx-x,2)+math.pow(my-y,2)) < self.size
    
    def update(self, view, controller):
        (x, y) = self.pos
        view.win.blit(self.surf, (x - self.size , y - self.size//2))

class Path:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ofs = [ random.randint(-i//4,i//4) for i in range(64,0,-1) ]

    def recpath(self, a, b, o, l):
        (ax, ay) = a
        (bx, by) = b
        if l == 1:
            return [ [ ax, ay ] ]
        c = ((ax+bx)//2 + self.ofs[o],(ay+by)//2 + self.ofs[o+1])
        path = self.recpath(a, c, o + 2, l // 2)
        path.extend(self.recpath(c, b, o + 2 + len(path), l // 2))
        if l == 16:
            path.append([ bx, by ])
        return path
  
    def update(self, view, controller):
        self.segments = self.recpath(self.a.pos, self.b.pos, 0, 16)
        pygame.draw.lines(view.win, (160,255,220), False, self.segments, 4)
                

class Background:
    def __init__(self):
        pass

    def update(self, view, controller):
        view.win.fill((0,0,0))

class Explorer:
    def __init__(self, caves, map, route, spawn):
        self.moving = True
        self.caves = caves
        self.map = map
        self.route = route
        self.node = self.route[0]
        self.path = map[route[0]][route[1]]
        self.idx = 0
        self.ofs = 0
        self.spawn = spawn
        self.color = (random.randint(20,60), random.randint(20,80), random.randint(20,120))
        self.surf = pygame.Surface((40,20), pygame.SRCALPHA)       
        PI = math.pi
        pygame.draw.ellipse(self.surf, self.color, [0,0,40,20])
        pygame.draw.arc(self.surf, (220,200,80), [0,0,40,20], 0, 2*PI, 2)
        for l in range(4):
            dim = 5*((16-l*4)%16)
            pygame.draw.arc(self.surf, (240-dim,200-dim,160-dim), [4+l*8,8,5,5],0,2*PI,4)
        print("Explorer route: ", route)

    def update(self, view, controller):        
        if self.path and controller.animate:
            self.ofs = (self.ofs + 1) % len(self.path.segments)
        
        if self.path and controller.animate and self.ofs == 0:
            self.idx += 1
            self.node = self.route[self.idx]
            if self.idx + 1 < len(self.route):
                self.path = self.map[self.route[self.idx]][self.route[self.idx+1]]
            else:
                self.path = None
        
        if self.path:
            if self.node == self.path.a.name:
                self.pos = tuple(self.path.segments[self.ofs])
            else:
                self.pos = tuple(self.path.segments[len(self.path.segments)-self.ofs-1])
            (x, y) = self.pos
        
            view.win.blit(self.surf, (x-20, y-10))
            self.spawn.ping()
        else:
            self.moving = False


class Spawn:
    def __init__(self, caves, map, routes):
        self.caves = caves
        self.map = map
        self.routes = routes
        self.tick = 0
        self.maxtick = 120
        self.ei = 0
        self.last = " (None) "
        self.moving = 0

    def ping(self):
        self.moving += 1

    def update(self, view, controller):
        if controller.animate:
            if self.tick <= 0 and self.ei < len(self.routes):
                print("Spawn explorer",self.ei)
                controller.add(Explorer(self.caves, self.map, self.routes[self.ei], self))
                self.last = " -> ".join(self.routes[self.ei])
                self.ei += 1
                if self.maxtick > 60:
                    self.maxtick -= 15
                elif self.maxtick > 30:
                    self.maxtick -= 5
                elif self.maxtick > 15:
                    self.maxtick -= 3
                elif self.maxtick > 7:
                    self.maxtick -= 2
                else:
                    self.maxtick -= 1

                self.tick = max(self.maxtick,1)
                self.moving += 1
            else:
                self.tick -= 1
                
        view.font.render_to(view.win, (10, 1040), "Active boats: {} / {}".format(self.moving, self.ei), (200, 240, 200))
        view.font.render_to(view.win, (10, 1060), "Last routed: {}".format(self.last), (200, 240, 200))
            
        if controller.animate and self.moving == 0:
            controller.animate = False
        self.moving = 0


def cost(node):
    return 0 if node[0] >= 'A' and node[0] <= 'Z' else 1    

def explore(map, node, visited, max, path):
    visited[node] += cost(node)
    if visited[node] == 2 and node != "start":
        max -= 1
    path.append(node)
    paths = []
    if node == "end":
        paths.append(path.copy())
    else:
        for next in filter(lambda n: visited[n] < max, map[node].keys()):
            paths.extend(explore(map, next, visited, max, path))
    path.pop()
    visited[node] -= 1
    if visited[node] == 1:
        max += 1
    return paths


def init(my_dir, controller, font):
    caves = {}
    map = {}
    visited = {}
    controller.add(Background())
    with open(my_dir + "/input/day12.txt") as f:
        for l in f.read().splitlines():
            (a, b) = tuple(l.split("-"))
            if a not in caves:
                caves[a] = Cave(a, font)
                map[a] = {}
                visited[a] = 0
            if b not in caves:
                caves[b] = Cave(b, font)
                map[b] = {}
                visited[b] = 0
            path = Path(caves[a], caves[b])
            map[a][b] = path
            map[b][a] = path
            controller.add(path)
    # stored positions
    names = [ "fs","end","he","DX","start","pj","zg","sl","RW","WI" ]
    poses = [(369, 750),(968, 1011),(989, 570),(368, 269),(988, 49),
             (984, 273),(1644, 697),(1643, 936),(1632, 258),(999, 795)]
    for i in range(len(names)):
        caves[names[i]].pos = poses[i]
    for c in caves.values():
        controller.add(c, clickable=True)
    visited["start"] = 1
    paths = explore(map, "start", visited, 2, [])
    # random.shuffle(paths)
    print(len(paths))
    controller.add(Spawn(caves, map, paths))
    return caves

view = View(1920,1080,30)
view.setup("Day 12")
controller = Controller(start_anim=False)
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
caves = init(my_dir, controller, view.font)
view.record(my_dir + "/day12.mp4")
controller.run(view)
for c in caves.values():
    print("pos[{}]={}".format(c.name, c.pos)) 

