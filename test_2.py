import pygame

pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 250
x, y = 50, 250
acceleration = 0

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

while True:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y -= 20
                acceleration = 0

    acceleration += 0.5
    y += 2 * acceleration

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), (x, y, 20, 20))

    pygame.display.update()
