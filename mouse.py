import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400
sc = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

sc.fill(COLOR_BLACK)
while True:
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == pygame.BUTTON_LEFT:
                pos_0 = i.pos
    if pygame.mouse.get_pressed()[0]:
        pos_1 = pygame.mouse.get_pos()
        pygame.draw.line(sc, COLOR_RED, pos_0, pos_1, 3)
        pos_0 = pos_1
    pygame.display.update()
    clock.tick(FPS)
