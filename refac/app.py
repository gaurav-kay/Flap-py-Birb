import pygame

from refac.Birb import Birb
from CONSTANTS import WIN_WIDTH, WIN_HEIGHT
from refac.Pipes import PipeSystem

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")
font = pygame.font.SysFont("Helvetica", 40)
game_over = False

pipes = PipeSystem()
birb = Birb()


def init_world():
    global pipes, birb
    pipes = PipeSystem()
    birb = Birb()


def run_as_human():
    # init world
    # reset score, init pipes, birds, text
    init_world()

    while True:
        jump = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump = True
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # pass
                # init world , reset world
                init_world()

        # update
        # update bird
        birb.update(jump)
        # update pipes
        pipes.update()
        # update score

        # collision check (update after collision), collision is a gamesystem responsibility, but for convenience, placing in Birb class
        # if check_collision(birb, pipes.get_nearest_pipe()):
        #     birb.dead = True
        birb.check_collision(pipes.get_nearest_pipe())

        # draw
        win.fill(color=(0, 0, 0))
        # draw bird
        birb.draw(win)
        # draw pipes
        pipes.draw(win)
        # draw score
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    run_as_human()