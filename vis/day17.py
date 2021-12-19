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

import re
import math
import pygame
from common import View, Controller


class Tracker:
    def __init__(self, line):
        m = re.search(r'target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)', line)
        self.x0, self.x1, self.y1, self.y0 = [int(m.group(i)) for i in range(1, 5)]
    
    def rect(self):
        return (8*self.x0, 8*self.x1, 600-4*self.y0, 600-4*self.y1)

    def trace(self, vx, vy):
        track = [(0, 600)]
        x = y = m = 0
        while True:
            x += vx
            y += vy
            track.append((8*x, 600-4*y))
            m = max(y, m)
            if x >= self.x0 and x <= self.x1 and y >= self.y1 and y <= self.y0:
                return track
            vy -= 1
            vx = max(0, vx-1)
            if (vx == 0 and x < self.x0) or x > self.x1 or y < self.y1:
                return None

    def yrange(self, vx):
        td = vx * (vx + 1) // 2
        if td >= self.x0 and td <= self.x1:
            xsmin = vx - int(math.sqrt((td-self.x0)*2))
            return range(self.y1//xsmin + (xsmin-1)//2, -self.y1 + 1)
        elif td > self.x1:
            tx = 0
            tvx = vx
            while tx < self.x0:
                tx += tvx
                tvx -= 1
            xsmin = vx - tvx
            while tx < self.x1 + 1:
                tx += tvx
                tvx -= 1
            xsmax = vx - tvx
            return range(self.y1//xsmin + (xsmin-1)//2, self.y0//xsmax + (xsmax+1)//2 + 1)
        else:
            return []

    def alltracks(self):
        vxmin = int(math.sqrt(self.x0*2))
        vxmax = self.x1
        tracks = []
        for vx in range(vxmin, vxmax + 1):
            for vy in self.yrange(vx):
                t = self.trace(vx, vy)
                if t:
                    tracks.append(t)
        return tracks


class Plotter:
    def __init__(self, tracer):
        self.tracer = tracer
        self.tracks = tracer.alltracks()

    def update(self, view, controller):
        if view.frame >= len(self.tracks):
            controller.animate = False
        if not controller.animate:
            return
        
        view.win.fill((0,0,0))
        (x0, x1, y0, y1) = self.tracer.rect()
        pygame.draw.rect(view.win, (180, 180, 240), (x0, y0, x1-x0, y1-y0), 1)
        for tidx in range(max(view.frame-160,0),view.frame+1):
            d = view.frame - tidx
            col1 = (180 - d , 180 - d , 250 - d - d//2)
            col2 = (220 - d , 220 - d , 200 - d )
            track = self.tracks[tidx]
            prev = track[0]
            for point in track:
                (x, y) = point
                pygame.draw.line(view.win, col1, prev, point, 1)
                pygame.draw.rect(view.win, col2, (x-2, y-2, 4, 4))
                prev = point


def init(controller):
    with open(controller.workdir() + "/input/day17.txt") as f:
        tracker = Tracker(f.readline())
        controller.add(Plotter(tracker))
    return controller


view = View(1920, 1080, 30)
view.setup("Day 17")
controller = Controller()
init(controller).run(view)
