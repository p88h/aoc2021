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
import math

pygame.init()
W = 1280
H = 720
C = 2*H//3
S = 10
B = W // S
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("AOC")

run = True
hmap = []
with open("../input/day01.txt") as f:
    hmap = list(map(int, f.read().splitlines()))
ofs = 0
clock = pygame.time.Clock()
PI = math.pi
hover = H//4
a = max(hmap[0:B//2])
h = C - (a - hmap[10]) - hover
anim = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        anim = True
    if keys[pygame.K_SPACE]:
        anim = False

    win.fill((0, 0, 0))
    b = max(hmap[ofs:ofs+B//2])
    if b > a + 6:
        b = a + 6
    if b < a:
        b = a
    a = b
    h1 = C - (a - hmap[ofs+10]) - hover
    if h1 > h + 8:
        h += 2
    if h1 < h- 8:
        h -= 2
    for p in range(1,B):
        x0 = S*(p-1)
        y0 = C-(a-hmap[ofs+p-1])
        x1 = S*p
        y1 = C-(a-hmap[ofs+p])
        c = (140,140,140)
        w = 1
        if y1 > y0 and p > 20 and p < 80:
            c = (160,255,160)
            w = 2
        pygame.draw.line(win, c, (x0, y0), (x1, y1) , w )
    pygame.draw.arc(win, (240,180,180), [120,h-20,40,20],0,2*PI,2)
    for l in range(4):
        dim = 5*((ofs+16-l*4)%16)
        pygame.draw.arc(win, (180-dim,240-dim,240-dim), [124+l*8,h-12,5,5],0,2*PI,4)
    for r in range(16):
        b = r*r+(ofs%16)
        pygame.draw.arc(win, (160-r*10,255-r*10,160-r*10),[160,h,b,b], 3*PI/2, 2*PI)
    if anim and ofs + B < len(hmap):
        ofs = ofs + 1

    pygame.display.update()
    clock.tick(40)

pygame.quit()