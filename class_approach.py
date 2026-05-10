import pygame

from Birb import Birb
from CONSTANTS import WIN_HEIGHT, WIN_WIDTH, UPDATE_DELAY, PIPES_ON_SCREEN, POPULATION_SIZE
from Pipe import Pipe
from genetic import get_next_gen_birbs


def run(run_as_human=True):
    game_over = False
    pygame.init()
    pygame.font.init()
    # clock = pygame.time.Clock()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flap-py birb")
    font = pygame.font.SysFont("Helvetica", 40)

    Pipe.init_pipes()

    Birb.birbs = [Birb() for _ in range(POPULATION_SIZE)] if not run_as_human else [Birb()]

    while True:  # until game window is open. sort of like a game window driver
        pygame.event.poll()  # :) (!) TODO: look at why it should be there

        pygame.time.delay(UPDATE_DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if not run_as_human:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # spawn new generation
                        for birb in Birb.birbs:
                            birb.dead = True
            if run_as_human:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Birb.birbs[0].jump()

        if not run_as_human:
            if not game_over:
                for birb in Birb.birbs:
                    flap_confidence = birb.brain.forward(birb.get_inputs())
                    if flap_confidence > 0.5:
                        birb.jump()

        # update and draw
        win.fill(color=(0, 0, 0))

        for pipe in Pipe.pipes:
            pipe.update(win, game_over)

        for birb in Birb.birbs:
            birb.update(win)

        Birb.draw_score(win, font, run_as_human)

        game_over = all([birb.dead for birb in Birb.birbs])

        if game_over and run_as_human == False:
            # wait for input and evolve and continue
            # collect stats of prev population
            # evolve
                # select top
                # crossover/breed
                # mutate
            pygame.time.delay(UPDATE_DELAY * 10)
            # once game_over, update fitness final time
            for birb in Birb.birbs:
                birb.update_fitness()
            Pipe.init_pipes()
            Birb.birbs = get_next_gen_birbs(Birb.birbs, Birb.max_score)
            for birb in Birb.birbs:
                birb.reset_birb()  # reset to init positions and conditions
            game_over = False

        if len(Pipe.pipes) < PIPES_ON_SCREEN:
            Pipe.add_pipe()

        pygame.display.update()
        # clock.tick(60)  # TODO: set clock tick, but alter this after updating speeds etc and removing time delay


if __name__ == '__main__':
    run(run_as_human=True)
    # run(run_as_human=False)
