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


def bbox(idx):
    return (20 + 160 * (idx % 12), 18 + 120 * (idx // 12))


class Player:
    def __init__(self, lines, idx) -> None:
        self.idx = idx
        self.pos = bbox(idx)
        self.numbers = []
        self.marked = [False] * 25
        self.anim = None
        self.won = False
        for l in lines:
            self.numbers.extend(map(int, l.split()))

    def update(self, view, controller):
        for i in range(len(self.numbers)):
            (x, y) = self.pos
            x += 24 * (i % 5)
            y += 16 * (i // 5)
            text = "{:2d}".format(self.numbers[i])
            if i == self.anim:
                col = (200, 250, 250) if view.frame % 2 == 0 else (120, 120, 120)
            else:
                col = (200, 240, 200) if self.marked[i] else (160, 160, 160)
            view.font.render_to(view.win, (x, y), text, col)
        (x, y) = self.pos
        if self.won:
            if self.anim:
                col = (200, 250, 250) if view.frame % 2 == 0 else (250, 200, 200)
            else:
                col = (255, 255, 255)
            view.font.render_to(view.win, (x+24, y+80), "B I N G O", col)

    def mark(self, card, server):
        self.anim = None
        if self.won:
            return
        if card in self.numbers:
            self.anim = self.numbers.index(card)
            self.marked[self.anim] = True
            for p in range(5):
                h = True
                for r in range(5):
                    h = h and self.marked[p * 5 + r]
                v = True
                for r in range(5):
                    v = v and self.marked[p + r * 5]
                if h or v:
                    self.won = True
            if self.won:
                score = 0
                for i in range(len(self.numbers)):
                    if not self.marked[i]:
                        score += self.numbers[i]
                server.addwinner(self.idx, score * card)


class Server:
    def __init__(self, cards, players):
        self.cards = cards
        self.players = players
        self.pos = bbox(100)
        print("bbox: {}".format(self.pos))
        self.idx = 0
        self.anim = []
        self.winners = []

    def update(self, view, controller):
        if view.frame % 10 == 0:
            if self.idx == len(self.cards):
                controller.animate = False
                return
            if len(self.anim) == 4:
                self.anim.pop()
            self.anim.insert(0, self.cards[self.idx])
            self.rank = len(self.winners) + 1
            for player in self.players:
                player.mark(self.cards[self.idx], self)
            self.idx += 1
        view.win.fill((0, 0, 0))
        (x, y) = self.pos
        view.font.render_to(view.win, (x, y), "Mark:", (255, 255, 255))
        x += 20
        for i in range(len(self.anim)):
            text = "{:2d}".format(self.anim[i])
            c = 240 / (i + 1)
            view.font.render_to(view.win, (x, y + (i + 1) * 16), text, (c, c, c))
        if view.frame % 2 == 0 and view.frame % 10 < 5:
            pygame.draw.rect(view.win, (255, 255, 255), (x - 4, y + 4, 24, 16), 2)
        x += 80
        if len(self.winners) == 0:
            return
        view.font.render_to(view.win, (x, y), "Winners:", (255, 255, 255))
        start = 0
        if len(self.winners) > 29:
            start = len(self.winners) - 29
        p = 0
        for i in range(start, len(self.winners)):
            (rank, id, score) = self.winners[i]
            tag = "ELF" if rank == 100 else "SQUID"
            text = "{}. {} [{}]: {}".format(rank, tag, id, score)
            p += 1
            view.font.render_to(view.win, (x + 180 * (p // 5),
                                y + 16 * (p % 5)), text, (255, 255, 255))

    def addwinner(self, idx, score):
        self.winners.append((self.rank, idx, score))


view = View(1920, 1080, 16)
view.setup("Day 02")
controller = Controller()
players = []
with open(controller.workdir() + "/input/day04.txt") as f:
    cards = [int(c) for c in f.readline().split(",")]
    server = Server(cards, players)
    controller.add(server)
    buf = []
    for l in f.readlines():
        buf.append(l)
        if len(buf) == 6:
            p = Player(buf, len(players))
            controller.add(p)
            players.append(p)
            buf = []

controller.run(view)
