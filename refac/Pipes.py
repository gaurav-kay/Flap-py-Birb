from random import randint
from typing import List

import pygame

from CONSTANTS import WIN_HEIGHT, PIPE_GAP, PLAYER_RADIUS, PIPE_WIDTH, WIN_WIDTH, PIPES_ON_SCREEN, INTER_PIPE_DISTANCE, \
    PIPE_SPEED


class Pipe:
    def __init__(self, top_left_x, top_left_y):
        self.top_left_x = self.bottom_left_x = top_left_x
        self.top_left_y = self.top_right_y = top_left_y
        self.top_right_x = self.bottom_right_x = top_left_x + PIPE_WIDTH
        self.bottom_left_y = self.bottom_right_y = top_left_y + PIPE_GAP
        self.off_screen = False

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.top_left_x, 0, PIPE_WIDTH, self.top_right_y))
        pygame.draw.rect(win, (0, 255, 0),
                         (self.bottom_left_x, self.bottom_left_y, PIPE_WIDTH, WIN_HEIGHT - self.bottom_right_y))

    def update(self):
        self.top_left_x -= PIPE_SPEED
        self.top_right_x -= PIPE_SPEED
        self.bottom_left_x -= PIPE_SPEED
        self.bottom_right_x -= PIPE_SPEED

        if self.top_right_x <= 0:
            self.off_screen = True

class PipeSystem:
    def __init__(self):
        self.pipes: List[Pipe] = []
        top_value = randint(PLAYER_RADIUS, WIN_HEIGHT - PLAYER_RADIUS - PIPE_GAP)  # 20 is top buffer and 20 is bottom buffer
        self.pipes.append(Pipe(WIN_WIDTH, top_value))

        while len(self.pipes) < PIPES_ON_SCREEN:
            self.add_pipe()

    def add_pipe(self):
        top_value = randint(PLAYER_RADIUS, WIN_HEIGHT - PLAYER_RADIUS - PIPE_GAP)
        self.pipes.append(Pipe(
            self.pipes[-1].top_right_x + INTER_PIPE_DISTANCE,
            top_value
        ))

    def update(self):
        for pipe in self.pipes:
            pipe.update()
        self.pipes = [i for i in self.pipes if not i.off_screen]
        if len(self.pipes) < PIPES_ON_SCREEN:
            self.add_pipe()

    def draw(self, win):
        for pipe in self.pipes:
            pipe.draw(win)

    def get_closest_pipe(self):
        return self.pipes[0]  # for input, be cautious
