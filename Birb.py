from random import randint

import numpy as np
import pygame

from Pipe import Pipe
from big_brain import Network
from CONSTANTS import WIN_HEIGHT, PLAYER_RADIUS, GRAVITY, JUMP, PIPE_SPEED, WIN_WIDTH


class Birb:
    birbs = []
    max_score = 0
    generation = 1

    def __init__(self):
        self.x = 50
        self.y = WIN_HEIGHT // 2
        self.time_falling = 0
        self.dead = False
        self.pipes_crossed = set()
        self.fitness = 0
        self.brain = Network([2, 6, 6, 6, 1])
        self.rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

    def reset_birb(self):  # staticmethod? reset all birbs at once?  # TODO: this is being weird
        self.x = 50
        self.y = WIN_HEIGHT // 2
        self.time_falling = 0
        self.dead = False
        self.pipes_crossed = set()
        self.fitness = 0

    def jump(self):
        self.y -= JUMP
        self.time_falling = 0

    def update(self, win):  # tick()
        if self.dead:
            self.draw(win)
            return

        self.time_falling += 0.5
        self.y += int(GRAVITY * self.time_falling)

        if self.y >= WIN_HEIGHT:
            self.dead = True
        elif self.y <= 0:
            self.y = 0
            # update fitness
            self.fitness += int(PIPE_SPEED * 0.8)
        else:
            # update fitness
            self.fitness += PIPE_SPEED

        if Pipe.collision(self):
            self.dead = True  # TODO: implement jump only if not dead

        self.update_score()
        self.draw(win)

    def update_fitness(self):
        nearest_pipe = Pipe.pipes[0]
        self.fitness -= nearest_pipe.top_left_x

    def draw(self, win):
        if not self.dead:
            # print(id(self), (self.x, self.y))
            pygame.draw.ellipse(win, self.rgb, (int(self.x), int(self.y), PLAYER_RADIUS, PLAYER_RADIUS))

    def update_score(self):
        for pipe in Pipe.pipes:
            if self.x >= pipe.top_right_x:
                self.pipes_crossed.add(pipe)
                break

    @staticmethod
    def draw_score(win: pygame.display, font: pygame.font.SysFont, run_as_human: bool):
        max_score_birb = max(Birb.birbs, key=lambda x: len(x.pipes_crossed))
        Birb.max_score = len(max_score_birb.pipes_crossed)
        birbs_alive = len([_ for _ in Birb.birbs if not _.dead])

        if run_as_human:
            text = font.render(f"Score: {Birb.max_score}", True, (255, 255, 255))
        else:
            text = font.render(f"Generation: {Birb.generation} & Score: {Birb.max_score} & Alive: {birbs_alive}", True, (255, 255, 255))

        padding = 10
        win.blit(text, (WIN_WIDTH - text.get_width() - padding, padding))

    def get_inputs(self) -> np.ndarray:  # see
        nearest_pipe = Pipe.pipes[0]

        x = self.x
        y = self.y

        distances = [[((x - nearest_pipe.top_left_x) ** 2 + (y - nearest_pipe.top_left_y) ** 2) ** 0.5],
                     [((x - nearest_pipe.bottom_left_x) ** 2 + (y - nearest_pipe.bottom_left_y) ** 2) ** 0.5]]

        distances = np.array(distances)
        distances = distances.reshape((2, 1))

        return distances