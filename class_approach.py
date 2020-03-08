import pygame
from random import randint
import tracemalloc

tracemalloc.start()

WIN_HEIGHT = 500
WIN_WIDTH = 500
PLAYER_RADIUS = 20
UPDATE_DELAY = 100
PIPE_GAP = PLAYER_RADIUS * 3
PIPE_WIDTH = 40
INTER_PIPE_DISTANCE = 100
PIPE_SPEED = 7
PIPES_ON_SCREEN = 10
GRAVITY = 3


def collision(birb):
    global PLAYER_RADIUS
    # try clamp method
    for pipe in Pipe.pipes:
        if birb.x + PLAYER_RADIUS >= pipe.top_left_x and birb.y + PLAYER_RADIUS <= pipe.top_left_y or \
                birb.x + PLAYER_RADIUS >= pipe.bottom_left_x and birb.y +PLAYER_RADIUS >= pipe.bottom_left_y:
            return True
    return False


class Birb:
    JUMP = 30

    def __init__(self):
        self.x = 50
        self.y = 250
        self.time_falling = 0
        self.dead = False

    def jump(self):
        self.y -= Birb.JUMP
        self.time_falling = 0

    def update(self, win):  # tick()
        self.time_falling += 0.5
        self.y += GRAVITY * self.time_falling

        if self.y >= WIN_HEIGHT:
            self.dead = True
        if self.y <= 0:
            self.y = 0

        if collision(self):
            self.dead = True  # TODO: implement jump only if not dead

        self.draw(win)

    def draw(self, win):
        if self.dead:
            pygame.draw.ellipse(win, (255, 0, 0), (self.x, WIN_HEIGHT - PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS))
        else:
            pygame.draw.ellipse(win, (255, 255, 255), (self.x, self.y, PLAYER_RADIUS, PLAYER_RADIUS))


class Pipe:
    pipes = []

    def __init__(self, top_left_x, top_left_y):
        self.top_left_x = top_left_x
        self.top_left_y = self.top_right_y = top_left_y
        self.top_right_x = top_left_x + PIPE_WIDTH
        self.bottom_left_x = top_left_x
        self.bottom_left_y = self.bottom_right_y = top_left_y + PIPE_GAP
        self.bottom_right_x = self.top_right_x
        self.off_screen = False

    def update(self, win):
        self.top_left_x -= PIPE_SPEED
        self.top_right_x -= PIPE_SPEED
        self.bottom_left_x -= PIPE_SPEED
        self.bottom_right_x -= PIPE_SPEED

        self.draw(win)

        if self.top_right_x <= 0:
            print("deleted")
            self.off_screen = True

        Pipe.pipes = [i for i in Pipe.pipes if not i.off_screen]

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.top_left_x, 0, PIPE_WIDTH, self.top_right_y))
        pygame.draw.rect(win, (0, 255, 0), (self.bottom_left_x, self.bottom_left_y, PIPE_WIDTH, WIN_HEIGHT - self.bottom_right_y))

    @staticmethod
    def add_pipe():
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
        Pipe.pipes.append(Pipe(
            Pipe.pipes[-1].top_right_x + PIPE_WIDTH + INTER_PIPE_DISTANCE,
            top_value
        ))

    @staticmethod
    def init_pipes():
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
        Pipe.pipes.append(Pipe(WIN_WIDTH, top_value))

        while len(Pipe.pipes) < PIPES_ON_SCREEN:
            top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
            Pipe.pipes.append(Pipe(
                Pipe.pipes[-1].top_right_x + PIPE_WIDTH + INTER_PIPE_DISTANCE,
                top_value
            ))


pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")

birb1 = Birb()

Pipe.init_pipes()

while True:  # until game window is open. sort of like a game window driver
    win.fill((0, 0, 0))
    pygame.time.delay(UPDATE_DELAY)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            tracemalloc.stop()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birb1.jump()

    if len(Pipe.pipes) < PIPES_ON_SCREEN:
        Pipe.add_pipe()

    print("len", len(Pipe.pipes))

    for pipe in Pipe.pipes:
        pipe.update(win)

    birb1.update(win)

    pygame.display.update()
