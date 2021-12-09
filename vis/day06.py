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

class Background:
    def __init__(self):
        pass

    def update(self, view, controller):
        if view.frame == 800:
            controller.animate = False
        text = "Day: {} Fish: {}".format(view.frame // 10, len(controller.objects) - 1)
        view.win.fill((0,0,0))
        view.font.render_to(view.win, (10, 16), text, (255, 255, 255))

def rndmod(value, factor, limit):
    (a, b) = limit
    value += random.randint(-factor, factor)
    value = max(a, value)
    value = min(b, value)
    return value

def posmod(view, pos, factor = 0):
    (x, y) = pos
    x = rndmod(x, factor, (5, view.width-5))
    y = rndmod(y, factor, (40, view.height-5))
    return (x,y)

class Fish:
    def __init__(self, counter, pos = None, col = None):
        self.pos = pos
        self.col = col if col else (random.randint(160, 255), random.randint(160, 255), random.randint(160, 255))
        self.counter = counter

    def update(self, view, controller):
        if not self.pos:
            self.pos = (random.randint(5, view.width), random.randint(5, view.height))
        (x, y) = posmod(view, self.pos, 2)
        if view.frame % 10 == 9:
            if self.counter == 0:
                self.counter = 6
                dx = random.randint(-3,3)
                dy = random.randint(-3,3)
                (r, g, b) = self.col
                ncol = (rndmod(r, 5, (0, 255)), rndmod(g, 5, (0, 255)), rndmod(b, 5, (0, 255)))
                controller.add(Fish(9, (x + dx, y + dy), ncol))
                x -= dx
                y -= dy
            else:
                self.counter -= 1

        mass = 9 - self.counter

        pygame.draw.circle(view.win, self.col, (x, y), mass, 2)
        if (mass > 2):
            pygame.draw.line(view.win, self.col, (x-mass-4, y-4), (x-mass-4, y+4), 2)
            pygame.draw.line(view.win, self.col, (x-mass-4, y-4), (x-mass, y), 2)
            pygame.draw.line(view.win, self.col, (x-mass-4, y+4), (x-mass, y), 2)
        if (mass > 5):
            pygame.draw.line(view.win, self.col, (x+mass/2, y-1), (x+mass/2+2, y-1), 2)
        self.pos = (x, y)


def init(my_dir, controller):
    controller.add(Background())
    with open(my_dir + "/input/day06.txt") as f:
        for f in map(int, f.readline().split(",")):            
            controller.add(Fish(f))


view = View(1920, 1080, 15)
view.setup("Day 02")
controller = Controller()
my_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
init(my_dir, controller)
view.record(my_dir + "/day6.mp4")
controller.run(view)
