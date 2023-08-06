import numpy as np
import pygame

from Pipe import Pipe
from big_brain import Network
from CONSTANTS import WIN_HEIGHT, PLAYER_RADIUS, GRAVITY, JUMP


class Birb:
    birbs = []
    maxes = []

    def __init__(self):
        self.x = 50
        self.y = WIN_HEIGHT // 2
        self.time_falling = 0
        self.dead = False
        self.pipes_crossed = set()
        self.fitness = 0
        self.generation = 0
        self.brain = self.net = Network([2, 6, 1])

    def jump(self):
        self.y -= JUMP
        self.time_falling = 0

    def update(self, win):  # tick()
        if self.dead:
            self.draw(win)
            return

        self.time_falling += 0.5
        self.y += GRAVITY * self.time_falling

        if self.y >= WIN_HEIGHT:
            self.dead = True
        if self.y <= 0:
            self.y = 0

        if Pipe.collision(self):
            self.dead = True  # TODO: implement jump only if not dead

        self.update_score()
        self.draw(win)

    def draw(self, win):
        if not self.dead:
            pygame.draw.ellipse(win, (255, 255, 255), (self.x, self.y, PLAYER_RADIUS, PLAYER_RADIUS))

    def update_score(self):
        for pipe in Pipe.pipes:
            if self.x >= pipe.top_right_x:
                self.pipes_crossed.add(pipe)
                break

    @staticmethod
    def draw_score(win, font):
        max_score_birb = max(Birb.birbs, key=lambda x: len(x.pipes_crossed))
        max_score = len(max_score_birb.pipes_crossed)

        text = font.render(f"Score: {max_score}", True, (255, 255, 255))

        if id(max_score_birb) not in Birb.maxes:
            win.blit(text, (0, 0))
            Birb.maxes = [id(max_score_birb)]
        else:
            win.blit(text, (0, 0))

    def get_inputs(self):  # see
        nearest_pipe = Pipe.pipes[0]

        x = self.x
        y = self.y

        distances = [[((x - nearest_pipe.top_left_x) ** 2 + (y - nearest_pipe.top_left_y) ** 2) ** 0.5],
                     [((x - nearest_pipe.bottom_left_x) ** 2 + (y - nearest_pipe.bottom_left_y) ** 2) ** 0.5]]

        distances = np.array(distances)
        distances = distances.reshape((2, 1))

        return distances