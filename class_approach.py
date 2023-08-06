import pygame
import tracemalloc

from Birb import Birb
from CONSTANTS import WIN_HEIGHT, WIN_WIDTH, UPDATE_DELAY, PIPES_ON_SCREEN, POPULATION_SIZE
from Pipe import Pipe

tracemalloc.start()


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
