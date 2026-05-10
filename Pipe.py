from random import randint
from typing import List

import pygame

from CONSTANTS import WIN_HEIGHT, WIN_WIDTH, PIPE_GAP, PIPE_WIDTH, INTER_PIPE_DISTANCE, PIPE_SPEED, PIPES_ON_SCREEN


class Pipe:
    pipes: List['Pipe'] = []

    def __init__(self, top_left_x, top_left_y):
        self.top_left_x = top_left_x
        self.top_left_y = self.top_right_y = top_left_y
        self.top_right_x = top_left_x + PIPE_WIDTH
        self.bottom_left_x = top_left_x
        self.bottom_left_y = self.bottom_right_y = top_left_y + PIPE_GAP
        self.bottom_right_x = self.top_right_x
        self.off_screen = False

    def update(self, win, game_over):
        if game_over:
            self.draw(win)
            return

        self.top_left_x -= PIPE_SPEED
        self.top_right_x -= PIPE_SPEED
        self.bottom_left_x -= PIPE_SPEED
        self.bottom_right_x -= PIPE_SPEED

        if self.top_right_x <= 0:
            self.off_screen = True

        Pipe.pipes = [i for i in Pipe.pipes if not i.off_screen]

        self.draw(win)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.top_left_x, 0, PIPE_WIDTH, self.top_right_y))
        pygame.draw.rect(win, (0, 255, 0),
                         (self.bottom_left_x, self.bottom_left_y, PIPE_WIDTH, WIN_HEIGHT - self.bottom_right_y))

    @staticmethod
    def add_pipe():
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
        Pipe.pipes.append(Pipe(
            Pipe.pipes[-1].top_right_x + PIPE_WIDTH + INTER_PIPE_DISTANCE,
            top_value
        ))

    @staticmethod
    def init_pipes():
        Pipe.pipes = []
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)  # 20 is top buffer and 20 is bottom buffer
        Pipe.pipes.append(Pipe(WIN_WIDTH, top_value))

        while len(Pipe.pipes) < PIPES_ON_SCREEN:
            Pipe.add_pipe()

    @staticmethod
    def collision(birb):
        # TODO: try clamp method
        # TODO: add birb radius to collision
        pipe = Pipe.pipes[0]
        if pipe.top_left_x <= birb.x <= pipe.top_right_x and birb.y <= pipe.top_left_y or \
                pipe.bottom_left_x <= birb.x <= pipe.bottom_right_x and birb.y >= pipe.bottom_left_y:
            return True
        return False
