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
import ffmpeg
import glob,os

pygame.init()
W = 1920
H = 1080
S = 1
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("AOC")

run = True
lines = []
file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
with open(file_path + "/input/day02.txt") as f:
    lines = f.read().splitlines()
idx = 0
(x0, y0) = (0, 0)
clock = pygame.time.Clock()
anim = False
win.fill((0, 0, 0))
pygame.event.clear()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                anim = True
            if event.key ==  pygame.K_SPACE:
                anim = False
            if event.key == pygame.K_ESCAPE:
                run = False
    
    if anim and idx < len(lines):
        l = lines[idx].split()
        v = int(l[1])
        (x1, y1) = (x0, y0)
        if l[0] == "forward":
            x1 += v
        if l[0] == "down":
            y1 += v
        if l[0] == "up":
            y1 -= v
        pygame.draw.line(win, (180,180,240), (x0 // S , y0 // S), (x1 // S, y1 // S), 2)
        (x0, y0) = (x1, y1)
        idx += 1
        pygame.image.save(win, "{}/snaps/{:04}.jpg".format(file_path, idx))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
snaps = "{}/snaps/*.jpg".format(file_path)
print("Now saving video")
ffmpeg.input(snaps, pattern_type='glob', framerate=60).output('day02.mp4').run()
print("Cleaning up snaps")
for f in glob.glob(snaps):
    os.remove(f)