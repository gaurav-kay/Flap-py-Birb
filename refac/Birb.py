from random import randint

import pygame

from CONSTANTS import WIN_HEIGHT, JUMP, PLAYER_RADIUS, GRAVITY, PIPE_SPEED, PLAYER_OFFSET
from big_brain import Network
from refac.Pipes import Pipe


# class Population:
#     def __init__(self):
#         self.birbs =

class Birb:
    def __init__(self):
        self.x = PLAYER_OFFSET
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

        if self.y + PLAYER_RADIUS >= WIN_HEIGHT:
            self.dead = True
            self.y = WIN_HEIGHT - PLAYER_RADIUS
        elif self.y - PLAYER_RADIUS <= 0:
            self.y = PLAYER_RADIUS

        # pipe related position constraints - Y axis only, X axis is handled by dead check
        if self.y - PLAYER_RADIUS <= closest_pipe.top_left_y and self.x + PLAYER_RADIUS >= closest_pipe.top_left_x \
                and self.x - PLAYER_RADIUS <= closest_pipe.top_right_x:
            self.y = closest_pipe.top_left_y + PLAYER_RADIUS
        if self.y + PLAYER_RADIUS >= closest_pipe.bottom_left_y and self.x + PLAYER_RADIUS >= closest_pipe.bottom_left_x \
                and self.x - PLAYER_RADIUS <= closest_pipe.bottom_right_x:
            self.y = closest_pipe.bottom_left_y - PLAYER_RADIUS

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
        # if pipe.top_left_x <= self.x <= pipe.top_right_x and self.y <= pipe.top_left_y or \
        #         pipe.bottom_left_x <= self.x <= pipe.bottom_right_x and self.y >= pipe.bottom_left_y:
        #     self.dead = True
        # else:
        #     self.dead = False or self.dead

        if pipe.top_left_x <= (self.x + PLAYER_RADIUS) <= pipe.top_right_x and (self.y + PLAYER_RADIUS) <= pipe.top_left_y or \
                pipe.bottom_left_x <= (self.x + PLAYER_RADIUS) <= pipe.bottom_right_x and (self.y + PLAYER_RADIUS) >= pipe.bottom_left_y:
            self.dead = True
        elif pipe.top_left_x <= (self.x - PLAYER_RADIUS) <= pipe.top_right_x and (self.y + PLAYER_RADIUS) <= pipe.top_left_y or \
                pipe.bottom_left_x <= (self.x - PLAYER_RADIUS) <= pipe.bottom_right_x and (self.y + PLAYER_RADIUS) >= pipe.bottom_left_y:
            self.dead = True
        elif pipe.top_left_x <= (self.x + PLAYER_RADIUS) <= pipe.top_right_x and (self.y - PLAYER_RADIUS) <= pipe.top_left_y or \
                pipe.bottom_left_x <= (self.x + PLAYER_RADIUS) <= pipe.bottom_right_x and (self.y - PLAYER_RADIUS) >= pipe.bottom_left_y:
            self.dead = True
        elif pipe.top_left_x <= (self.x - PLAYER_RADIUS) <= pipe.top_right_x and (self.y - PLAYER_RADIUS) <= pipe.top_left_y or \
                pipe.bottom_left_x <= (self.x - PLAYER_RADIUS) <= pipe.bottom_right_x and (self.y - PLAYER_RADIUS) >= pipe.bottom_left_y:
            self.dead = True
        else:
            self.dead = False or self.dead


    def draw(self, win):
        # if not self.dead:
        rect_top_left_x = self.x - PLAYER_RADIUS
        rect_top_left_y = self.y - PLAYER_RADIUS
        pygame.draw.ellipse(win, self.rgb, (int(rect_top_left_x), int(rect_top_left_y), 2 * PLAYER_RADIUS, 2 * PLAYER_RADIUS))
