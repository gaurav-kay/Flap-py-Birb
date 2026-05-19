import pygame

from genetic import get_next_gen_birbs
from refac.Birb import Birb
from refac.Pipes import PipeSystem
from CONSTANTS import WIN_WIDTH, WIN_HEIGHT, POPULATION_SIZE, UPDATE_DELAY

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")
font = pygame.font.SysFont("Helvetica", 40)


def draw_score(score: int, generation=None, birbs_alive=None):
    if generation:
        text = font.render(f"Generation: {generation} & Score: {score} & Alive: {birbs_alive}", True, (255, 255, 255))
    else:
        text = font.render(f"Score: {score}", True, (255, 255, 255))
    padding = 10
    win.blit(text, (WIN_WIDTH - text.get_width() - padding, padding))


def run_as_human():
    # init world
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
        draw_score(birb.score)
        pygame.display.update()

        clock.tick(60)

def run_as_ai():
    pipes = PipeSystem()
    birbs = [Birb() for _ in range(POPULATION_SIZE)]
    game_over = False
    generation = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = True


        if game_over:
            pygame.display.update()
            pygame.time.delay(UPDATE_DELAY * 10)
            for birb in birbs:
                birb.update_fitness_after_game_over(pipes.get_closest_pipe())
            pipes = PipeSystem()  # TODO: consider option of keeping same pipe system with same seed?
            birbs = get_next_gen_birbs(birbs)
            for birb in birbs:
                birb.reset()  # reset to init positions and conditions
            generation += 1
            game_over = False
            continue


        # update
        # update bird
        for birb in birbs:
            jump = birb.handle_ai(pipes.get_closest_pipe())
            birb.update(jump, pipes.get_closest_pipe())
        # update pipes
        pipes.update()
        # update score

        # collision check (update after collision), collision is a gamesystem responsibility, but for convenience, placing in Birb class
        for birb in birbs:
            birb.check_collision(pipes.get_closest_pipe())

        # update game state
        game_over = all([birb.dead for birb in birbs])

        # draw
        win.fill(color=(0, 0, 0))
        # draw bird
        for birb in birbs:
            birb.draw(win)
        # draw pipes
        pipes.draw(win)
        # draw score
        score = max(birbs, key=lambda x: x.score).score
        birbs_alive = len(list(filter(lambda x: not x.dead, birbs)))
        draw_score(score, generation, birbs_alive)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    # run_as_human()
    run_as_ai()
