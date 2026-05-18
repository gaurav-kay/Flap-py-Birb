from collections import namedtuple
from random import randint

import pygame

from CONSTANTS import WIN_HEIGHT, JUMP, PLAYER_RADIUS, GRAVITY, PIPE_SPEED
from big_brain import Network
from refac.Pipes import Pipe


# class Population:
#     def __init__(self):
#         self.birbs =

class Birb:
    def __init__(self):
        self.x = 50
        self.y = WIN_HEIGHT // 2
        self.time_falling = 0
        self.dead = False
        self.prev_pipe_crossed = None
        self.score = 0
        self.fitness = 0
        self.brain = Network([2, 6, 1])
        self.rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

    def update_position(self, jump: bool, closest_pipe: Pipe):
        if jump:
            self.time_falling = 0
            self.y -= JUMP
        else:
            self.time_falling += 0.5
            self.y += int(GRAVITY * self.time_falling)

        if self.y >= WIN_HEIGHT:
            self.dead = True
        elif self.y <= 0:
            self.y = 0

        # pipe related position constraints
        # if self.y + PLAYER_RADIUS <= closest_pipe.top_left_y:
        #     self.y =

    def update_fitness(self):
        if self.y <= 0:
            self.fitness += int(PIPE_SPEED * 0.8)
        elif self.y < WIN_HEIGHT:
            self.fitness += PIPE_SPEED

    def update_score(self, closest_pipe: Pipe):
        if self.x > closest_pipe.top_right_x:
            if self.prev_pipe_crossed is not closest_pipe:
                self.score += 1
                self.fitness += PIPE_SPEED * 0.5
                self.prev_pipe_crossed = closest_pipe

    def update(self, jump: bool, closest_pipe: Pipe):
        if self.dead:
            return

        self.update_position(jump, closest_pipe)
        self.update_score(closest_pipe)
        self.update_fitness()

    def check_collision(self, pipe: Pipe):
        if pipe.top_left_x <= self.x <= pipe.top_right_x and self.y <= pipe.top_left_y or \
                pipe.bottom_left_x <= self.x <= pipe.bottom_right_x and self.y >= pipe.bottom_left_y:
            self.dead = True
        else:
            self.dead = False or self.dead

        # PLAYER_RADIUS = 0
        # Point = namedtuple("Point", ["x", "y"])
        # center = Point(self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS)
        # if pipe.top_left_x <= (center.x + PLAYER_RADIUS) <= pipe.top_right_x and (center.y + PLAYER_RADIUS) <= pipe.top_left_y or \
        #         pipe.bottom_left_x <= (center.x + PLAYER_RADIUS) <= pipe.bottom_right_x and (center.y + PLAYER_RADIUS) >= pipe.bottom_left_y:
        #     self.dead = True
        # elif pipe.top_left_x <= (center.x - PLAYER_RADIUS) <= pipe.top_right_x and (center.y + PLAYER_RADIUS) <= pipe.top_left_y or \
        #         pipe.bottom_left_x <= (center.x - PLAYER_RADIUS) <= pipe.bottom_right_x and (center.y + PLAYER_RADIUS) >= pipe.bottom_left_y:
        #     self.dead = True
        # elif pipe.top_left_x <= (center.x + PLAYER_RADIUS) <= pipe.top_right_x and (center.y - PLAYER_RADIUS) <= pipe.top_left_y or \
        #         pipe.bottom_left_x <= (center.x + PLAYER_RADIUS) <= pipe.bottom_right_x and (center.y - PLAYER_RADIUS) >= pipe.bottom_left_y:
        #     self.dead = True
        # elif pipe.top_left_x <= (center.x - PLAYER_RADIUS) <= pipe.top_right_x and (center.y - PLAYER_RADIUS) <= pipe.top_left_y or \
        #         pipe.bottom_left_x <= (center.x - PLAYER_RADIUS) <= pipe.bottom_right_x and (center.y - PLAYER_RADIUS) >= pipe.bottom_left_y:
        #     self.dead = True
        # else:
        #     self.dead = False or self.dead


    def draw(self, win):
        # if not self.dead:
        pygame.draw.ellipse(win, self.rgb, (int(self.x), int(self.y), PLAYER_RADIUS, PLAYER_RADIUS))
