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


# def init_world():
#     global pipes, birb
#     pipes = PipeSystem()
#     birb = Birb()


def draw_score(win, score: int):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    padding = 10
    win.blit(text, (WIN_WIDTH - text.get_width() - padding, padding))


def run_as_human():
    # init world
    # reset score, init pipes, birds, text
    # init_world()
    pipes = PipeSystem()
    birb = Birb()
    game_over = False

    while True:
        jump = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump = True
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # init_world()
                # game_over = False
                run_as_human()

        if not game_over:  # skip over update if game over
            # update
            # update bird
            birb.update(jump, pipes.get_closest_pipe())
            # update pipes
            pipes.update()
            # update score

        # collision check (update after collision), collision is a gamesystem responsibility, but for convenience, placing in Birb class
        birb.check_collision(pipes.get_closest_pipe())

        # update game state
        game_over = birb.dead

        # draw
        win.fill(color=(0, 0, 0))
        # draw bird
        birb.draw(win)
        # draw pipes
        pipes.draw(win)
        # draw score
        draw_score(win, birb.score)
        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    run_as_human()