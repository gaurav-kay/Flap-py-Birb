import pygame
from random import randint

WIN_HEIGHT = 500
WIN_WIDTH = 500
PLAYER_RADIUS = 20
UPDATE_DELAY = 100
PIPE_GAP = PLAYER_RADIUS * 2.5
PIPE_WIDTH = 40
INTER_PIPE_DISTANCE = 50
PIPE_SPEED = 3


class Birb:
    JUMP = 25
    GRAVITY = 3

    def __init__(self):
        self.x = 50
        self.y = 250
        self.speed = 0
        self.dead = False

    def jump(self):
        self.y -= Birb.JUMP
        self.speed = 0

    def update(self, win):  # tick()
        self.speed += 0.5
        self.y += Birb.GRAVITY * self.speed

        if self.y >= WIN_HEIGHT:
            self.dead = True
        if self.y <= 0:
            self.y = 0

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
        self.bottom_left_y = self.bottom_right_y = top_left_y + INTER_PIPE_DISTANCE
        self.bottom_right_x = self.top_right_x
        # self.top_right_y = top_left_y + PIPE_WIDTH
        # self.bottom_left_x = self.bottom_right_x = self.top_right_x + PIPE_GAP
        # self.bottom_left_y = top_left_y + PIPE_GAP
        # self.bottom_right_y = self.bottom_left_y + PIPE_GAP + PIPE_WIDTH
        self.off_screen = False

    def update(self, win):
        self.top_left_x -= PIPE_SPEED
        self.top_right_x -= PIPE_SPEED
        self.bottom_left_x -= PIPE_SPEED
        self.bottom_right_x -= PIPE_SPEED

        self.draw(win)
        # if self.top_right_y <= 0:
        #     print("deleted")
        #     self.off_screen = True
        #     Pipe.pipes.remove(self)
        #     del self

    def draw(self, win):
        # pygame.draw.rect(win, (0, 255, 0), (self.top_right_x, self.top_right_y, 0, self.top_left_y))
        # print(0, self.top_left_y, self.top_right_x, self.top_right_y)
        # pygame.draw.rect(win, (0, 255, 0), (WIN_HEIGHT, self.bottom_right_y, self.bottom_left_x, self.bottom_left_y))
        # print(self.bottom_left_x, self.bottom_left_y, WIN_HEIGHT, self.bottom_right_y)
        pygame.draw.rect(win, (0, 255, 0), (self.top_left_x, 0, PIPE_WIDTH, self.top_right_y))
        print(0, self.top_left_y, self.top_right_x, self.top_right_y)
        pygame.draw.rect(win, (0, 255, 0), (self.bottom_left_x, self.bottom_left_y, PIPE_WIDTH, WIN_HEIGHT - self.bottom_right_y))
        print(self.bottom_left_x, self.bottom_left_y, WIN_HEIGHT, self.bottom_right_y)

    @staticmethod
    def add_pipe():
        pass

    @staticmethod
    def init_pipes():
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)

        Pipe.pipes.append(Pipe(WIN_WIDTH, top_value))

        # Pipe.pipes.append(Pipe(
        #     (top_value, top_value + PIPE_WIDTH),
        #     (top_value + PIPE_GAP, top_value + PIPE_GAP + PIPE_WIDTH)
        # ))

        while len(Pipe.pipes) < 5:
            top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)

            Pipe.pipes.append(Pipe(
                # top_value,
                # Pipe.pipes[-1].top_left_y + PIPE_WIDTH + INTER_PIPE_DISTANCE
                Pipe.pipes[-1].top_right_x + PIPE_WIDTH + INTER_PIPE_DISTANCE,
                top_value
            ))


pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")

birb1 = Birb()
birb2 = Birb()

Pipe.init_pipes()

while True:  # until game window is open. sort of like a game window driver
    win.fill((0, 0, 0))
    pygame.time.delay(UPDATE_DELAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birb1.jump()
            if event.key == pygame.K_DOWN:
                birb2.jump()

    if len(Pipe.pipes) < 5:
        Pipe.add_pipe()

    print(len(Pipe.pipes))

    for pipe in Pipe.pipes:
        pipe.update(win)

    # delete pipes off screen
    # Pipe.delete_pipes()

    birb1.update(win)
    birb2.update(win)

    pygame.display.update()
