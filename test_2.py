import pygame

pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 250
PLAYER_RADIUS = 20
UPDATE_DELAY = 100
x, y = 50, 250
acceleration = 0
ball_colour = (255, 255, 255)
game_over = False

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")

while not game_over:
    pygame.time.delay(UPDATE_DELAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y -= 25
                acceleration = 0

    print(x, y)

    if y >= WIN_HEIGHT:
        print("belowww")
        pygame.draw.ellipse(win, (255, 0, 0), (x, 480, PLAYER_RADIUS, PLAYER_RADIUS))
        pygame.display.update()
        break

    if y <= 0:
        print("up top haha")
        y = 0

    acceleration += 0.5
    y += 3 * acceleration

    win.fill((0, 0, 0))
    pygame.draw.ellipse(win, ball_colour, (x, y, PLAYER_RADIUS, PLAYER_RADIUS))

    pygame.display.update()

while True:
    pygame.time.delay(100)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
