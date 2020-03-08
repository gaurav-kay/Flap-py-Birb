import pygame

WIN_HEIGHT = 500
WIN_WIDTH = 500
PLAYER_RADIUS = 20
UPDATE_DELAY = 100


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

    def update(self):  # tick()
        self.speed += 0.5
        self.y += 3 * self.speed

        if self.y >= WIN_HEIGHT:
            self.dead = True
        if self.y <= 0:
            self.y = 0

        self.draw()

    def draw(self):
        if self.dead:
            pygame.draw.ellipse(win, (255, 0, 0), (self.x, WIN_HEIGHT - PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS))
        else:
            pygame.draw.ellipse(win, (255, 255, 255), (self.x, self.y, PLAYER_RADIUS, PLAYER_RADIUS))


pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flap-py birb")

birb1 = Birb()
birb2 = Birb()

while True:
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

    win.fill((0, 0, 0))
    birb1.update()
    birb2.update()

    pygame.display.update()
