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
from common import View, Controller


class Background:
    def __init__(self, base_path):
        self.pos = (0, 0)
        with open(base_path + "/input/day02.txt") as f:
            self.lines = f.read().splitlines()

    def update(self, view, controller):
        if view.frame >= len(self.lines) - 1:
            controller.animate = False

        idx = view.frame
        l = self.lines[idx].split()
        v = int(l[1])
        (x0, y0) = self.pos
        (x1, y1) = self.pos
        if l[0] == "forward":
            x1 += v
        if l[0] == "down":
            y1 += v
        if l[0] == "up":
            y1 -= v
        pygame.draw.line(view.win, (180, 180, 240), (x0, y0), (x1, y1), 2)
        self.pos = (x1, y1)


view = View()
view.setup("Day 02")
controller = Controller()
controller.add(Background(controller.workdir()))
controller.run(view)
