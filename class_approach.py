import pygame
from random import randint
import tracemalloc
import numpy as np
from big_brain import Network

tracemalloc.start()

WIN_HEIGHT = 500
WIN_WIDTH = 800
PLAYER_RADIUS = 20
UPDATE_DELAY = 100
PIPE_GAP = PLAYER_RADIUS * 6
PIPE_WIDTH = 40
INTER_PIPE_DISTANCE = 200
PIPE_SPEED = 15
PIPES_ON_SCREEN = 10
GRAVITY = 5
POPULATION_SIZE = 20
JUMP = 45


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
        top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
        Pipe.pipes.append(Pipe(WIN_WIDTH, top_value))

        while len(Pipe.pipes) < PIPES_ON_SCREEN:
            top_value = randint(20, WIN_HEIGHT - 20 - PIPE_GAP)
            Pipe.pipes.append(Pipe(
                Pipe.pipes[-1].top_right_x + PIPE_WIDTH + INTER_PIPE_DISTANCE,
                top_value
            ))

    @staticmethod
    def collision(birb):
        # try clamp method
        pipe = Pipe.pipes[0]
        if pipe.top_left_x <= birb.x <= pipe.top_right_x and birb.y <= pipe.top_left_y or \
                pipe.bottom_left_x <= birb.x <= pipe.bottom_right_x and birb.y >= pipe.bottom_left_y:
            return True
        return False


def handle_ai(win, font):
    for birb in Birb.birbs:
        flap_confidence = birb.brain.forward(birb.get_inputs())
        if flap_confidence > 0.5:
            birb.jump()

    game_over = all([birb.dead for birb in Birb.birbs])

    for pipe in Pipe.pipes:
        pipe.update(win, game_over)

    for birb in Birb.birbs:
        birb.update(win)

    Birb.draw_score(win, font)


def run(run_as_human=True):
    pygame.init()
    pygame.font.init()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flap-py birb")
    font = pygame.font.SysFont("Helvetica", 40)

    Pipe.init_pipes()

    Birb.birbs = [Birb() for _ in range(POPULATION_SIZE)] if not run_as_human else [Birb()]

    while True:  # until game window is open. sort of like a game window driver
        pygame.event.poll()  # :) (!)

        win.fill((0, 0, 0))
        pygame.time.delay(UPDATE_DELAY)

        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB",
              len([i for i in Birb.birbs if not i.dead]) if not run_as_human else None)

        if run_as_human:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    tracemalloc.stop()
                    exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Birb.birbs[0].jump()

            game_over = Birb.birbs[0].dead  # update game_over if all birbs are dead

            for pipe in Pipe.pipes:
                pipe.update(win, game_over)

            Birb.birbs[0].update(win)
            Birb.draw_score(win, font)
        else:
            handle_ai(win, font)

        if len(Pipe.pipes) < PIPES_ON_SCREEN:
            Pipe.add_pipe()

        pygame.display.update()


if __name__ == '__main__':
    run(run_as_human=False)
