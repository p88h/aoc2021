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
import glob
import os


class View:
    def __init__(self, W=1920, H=1080, FPS=60) -> None:
        self.width = W
        self.height = H
        self.fps = FPS
        self.save = False
        self.frame = 0

    def setup(self, title="AOC"):
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.win.fill((0, 0, 0))

    def record(self, output_path):
        self.save = True
        self.output_path = output_path
        self.tmp_path = os.path.dirname(output_path) + "/tmp/"

    def render(self, controller):
        for object in controller.objects:
            object.update(self, controller)
        
        pygame.display.update()
        self.clock.tick(self.fps)

        if controller.animate:
            self.frame += 1
            if self.save:
                pygame.image.save(self.win, "{}/frame_{:04}.jpg".format(self.tmp_path, self.frame))

    def finish(self):
        if not self.save:
            return
        print("Now saving video")
        snaps = "{}/frame_*.jpg".format(self.tmp_path)
        ffmpeg.input(snaps, pattern_type='glob', framerate=60).output(self.output_path).run()
        print("Cleaning up snaps")
        for f in glob.glob(snaps):
            os.remove(f)

class Controller:
    def __init__(self, start_anim = True) -> None:
        self.animate = start_anim
        self.quit = False
        self.objects = []
        pass

    def add(self, object):
        self.objects.append(object)

    def run(self, view):
        pygame.event.clear()
        while not self.quit:
            view.render(self)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.animate = not self.animate
                    if event.key == pygame.K_ESCAPE:
                        self.quit = True            
        pygame.quit()
        view.finish()        
